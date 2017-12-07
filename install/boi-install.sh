#!/bin/bash

BOI_DIR="/opt/boi"
BOI_CONFIG_DIR="$BOI_DIR/config"
BOI_LIB_DIR="$BOI_DIR/lib"
BOI_3P_DIR="$BOI_DIR/3p"
BOI_CLI_DIR="$BOI_DIR/cli"

BOI_EFS_DIR="$BOI_DIR/efs"
BOI_EFS_USERS_DIR="$BOI_EFS_DIR/users"
BOI_EFS_ZEPPELIN_DIR="$BOI_EFS_DIR/zeppelin"
BOI_EFS_ZEPPELIN_NB_DIR="$BOI_EFS_ZEPPELIN_DIR/notebook"

MYSQL_CONNECTOR_JAVA="mysql-connector-java-5.1.44-bin"
MYSQL_CONNECTOR_PYTHON="mysql-connector-python-2.1.7"

ZEPPELIN_DIR="/usr/lib/zeppelin"
ZEPPELIN_CONF_DIR="$ZEPPELIN_DIR/conf"
ZEPPELIN_BIN_DIR="$ZEPPELIN_DIR/bin"
ZEPPELIN_NB_DIR="/var/lib/zeppelin/notebook"

ARG_KEY_S3_URI="-s3uri"
ARG_KEY_NEW_SETUP="-new"

ARG_VALUE_S3_URI=""
ARG_VALUE_NEW_SETUP=0

#===============================================================================
#    ARGUMENTS PARSING
#===============================================================================
printf ">>> Validating arguments ...\n"

if [[ $# > 0 ]]; then

    while [[ "$1" != "" ]]; do

        case "$1" in
            "$ARG_KEY_S3_URI" )
                shift
                ARG_VALUE_S3_URI="$1"
                printf "Argument <%s>,Value <%s>\n" "$ARG_KEY_S3_URI" "$ARG_VALUE_S3_URI"
                ;;
            "$ARG_KEY_NEW_SETUP" )
                shift
                ARG_VALUE_NEW_SETUP=1
                printf "Argument <%s>,Value <%s>\n" "$ARG_KEY_NEW_SETUP" "$ARG_VALUE_NEW_SETUP"
                ;;
            * )
                printf "[ERROR] Invalid argument <%s>\n" "$1"
                exit 1
                ;;
        esac
        
        shift
    
    done

fi

if [[ "$ARG_VALUE_S3_URI" = "" ]]; then
    printf "[ERROR] Argument <%s> is missing or invalid.\n" "$ARG_KEY_S3_URI"
    exit 1
fi

printf "<<< Done.\n\n"

#===============================================================================
#    INSTALLING BOI
#===============================================================================
printf ">>> Installing BOI ...\n"

printf "> Setting up boi dir <%s> ... " "$BOI_DIR"
sudo mkdir -p "$BOI_DIR"
printf "done.\n"

printf "> Downloading <config> dir from <%s> to <%s> ... \n" "$ARG_VALUE_S3_URI/config" "$BOI_CONFIG_DIR"
sudo mkdir -p "$BOI_CONFIG_DIR"
sudo aws s3 cp "$ARG_VALUE_S3_URI/config/" "$BOI_CONFIG_DIR" --recursive
printf "done.\n"

printf "> Downloading <lib> dir from <%s> to <%s> ... \n" "$ARG_VALUE_S3_URI/lib" "$BOI_LIB_DIR"
sudo mkdir -p "$BOI_LIB_DIR"
sudo aws s3 cp "$ARG_VALUE_S3_URI/lib/" "$BOI_LIB_DIR" --recursive
printf "done.\n"

printf "> Downloading <3p> dir from <%s> to <%s> ... \n" "$ARG_VALUE_S3_URI/3p" "$BOI_3P_DIR"
sudo mkdir -p "$BOI_3P_DIR"
sudo aws s3 cp "$ARG_VALUE_S3_URI/3p/" "$BOI_3P_DIR" --recursive
printf "done.\n"

printf "> Downloading <cli> dir from <%s> to <%s> ... \n" "$ARG_VALUE_S3_URI/cli" "$BOI_CLI_DIR"
sudo mkdir -p "$BOI_CLI_DIR"
sudo aws s3 cp "$ARG_VALUE_S3_URI/cli/" "$BOI_CLI_DIR" --recursive
sudo aws s3 cp "$ARG_VALUE_S3_URI/boi-cli.py" "$BOI_DIR"
printf "done.\n"

printf "<<< Done.\n\n"

#===============================================================================
#    EFS SETUP
#===============================================================================
printf ">>> Setting up efs <%s> ... \n" "$BOI_EFS_DIR"

sudo mkdir -p "$BOI_EFS_DIR"
sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 $EFS_HOST:/ $BOI_EFS_DIR

if [[ $ARG_VALUE_NEW_SETUP = 1 ]]; then
    printf "> Setting up new install ... \n"
    sudo rm -rf $BOI_EFS_DIR/*
    sudo mkdir -p "$BOI_EFS_USERS_DIR"
    sudo mkdir -p "$BOI_EFS_ZEPPELIN_DIR"
    sudo mkdir -p "$BOI_EFS_ZEPPELIN_NB_DIR"
    sudo chmod -R o+w "$BOI_EFS_ZEPPELIN_DIR"
    printf "done.\n"
fi

printf "<<< Done.\n\n"

#===============================================================================
#    LOADING PROPERTIES
#===============================================================================
printf ">>> Loading Properties ...\n"

PROPERTIES_FILE="$BOI_CONFIG_DIR/properties.py"

function get_property {
    if [ -f $PROPERTIES_FILE ]; then
        PROP_KEY=$1
        PROP_VALUE=`cat $PROPERTIES_FILE | grep -sw "$PROP_KEY" | cut -d'=' -f2`
        PROP_VALUE=$(sed -e 's/^"//' -e 's/"$//' <<< "$PROP_VALUE")
        echo $PROP_VALUE
    else
        echo ""
    fi
}

BOI_ZEPPELIN_DB_HOST=$(get_property 'boi_zeppelin_db_host')
BOI_ZEPPELIN_DB_NAME=$(get_property 'boi_zeppelin_db_name')
BOI_ZEPPELIN_DB_USER=$(get_property 'boi_zeppelin_db_user')
BOI_ZEPPELIN_DB_PASSWORD=$(get_property 'boi_zeppelin_db_password')

EFS_HOST=$(get_property 'efs_host')

printf "<<< Done.\n\n"

#===============================================================================
#    PYTHON SETUP
#===============================================================================
printf ">>> Setting up python ...\n"

printf "> Installing pycrypto ... \n"
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install pycrypto
printf "done.\n"

printf "<<< Done.\n\n"

#===============================================================================
#    MYSQL SETUP
#===============================================================================
printf ">>> Setting up mysql ... \n"

printf "> Setting up mysql java connector ... \n"
sudo cp "$BOI_3P_DIR/mysql/$MYSQL_CONNECTOR_JAVA.jar" "$ZEPPELIN_DIR/lib/"
printf "done.\n"

printf "> Setting up mysql python connector ... \n"
CURRENT_DIR=$(pwd)
cd "$BOI_3P_DIR/mysql/"
sudo tar -xzf "$MYSQL_CONNECTOR_PYTHON.tar.gz"
cd "$MYSQL_CONNECTOR_PYTHON"
sudo python3 setup.py install
cd "$BOI_3P_DIR/mysql/"
sudo rm -rf "$MYSQL_CONNECTOR_PYTHON"
cd "$CURRENT_DIR"
printf "done.\n"

printf "<<< Done.\n\n"

#===============================================================================
#    ZEPPELIN SETUP
#===============================================================================
printf ">>> Setting up zeppelin ... \n"

printf "> Stopping zeppelin service ... \n"
sudo stop zeppelin
printf "done.\n"

printf "> Setting up <zeppelin-site.xml> ... \n"
sudo cp "$BOI_3P_DIR/zeppelin/conf/zeppelin-site.xml.template" "$ZEPPELIN_CONF_DIR/zeppelin-site.xml"
sudo chown zeppelin:zeppelin "$ZEPPELIN_CONF_DIR/zeppelin-site.xml"
printf "done.\n"

printf "> Setting up <zeppelin-env.sh> ... \n"
sudo cp "$BOI_3P_DIR/zeppelin/conf/zeppelin-env.sh.template" "$ZEPPELIN_CONF_DIR/zeppelin-env.sh"
sudo chown zeppelin:zeppelin "$ZEPPELIN_CONF_DIR/zeppelin-env.sh"
printf "done.\n"

printf "> Setting up <interpreter.json> ... \n"
sudo cp "$BOI_3P_DIR/zeppelin/conf/interpreter.json.template" "$ZEPPELIN_CONF_DIR/interpreter.json"
sudo chown zeppelin:zeppelin "$ZEPPELIN_CONF_DIR/interpreter.json"
printf "done.\n"

printf "> Setting up JDBC interpreter ... \n"
CURRENT_DIR=$(pwd)
cd "$ZEPPELIN_BIN_DIR"
sudo ./install-interpreter.sh --name jdbc
sudo cp $BOI_DIR/3p/zeppelin/interpreter/jdbc/* $ZEPPELIN_DIR/interpreter/jdbc/
cd "$CURRENT_DIR"
printf "done.\n"

printf "> Setting up <shiro.ini> ... \n"
sudo cp "$BOI_3P_DIR/zeppelin/conf/shiro.ini.template" "$ZEPPELIN_CONF_DIR/shiro.ini"
sudo chown zeppelin:zeppelin "$ZEPPELIN_CONF_DIR/shiro.ini"
sudo sed -i "s/ds.serverName=[^ ]*/ds.serverName=$BOI_ZEPPELIN_DB_HOST/g" "$ZEPPELIN_CONF_DIR/shiro.ini"
sudo sed -i "s/ds.databaseName=[^ ]*/ds.databaseName=$BOI_ZEPPELIN_DB_NAME/g" "$ZEPPELIN_CONF_DIR/shiro.ini"
sudo sed -i "s/ds.user=[^ ]*/ds.user=$BOI_ZEPPELIN_DB_USER/g" "$ZEPPELIN_CONF_DIR/shiro.ini"
sudo sed -i "s/ds.password=[^ ]*/ds.password=$BOI_ZEPPELIN_DB_PASSWORD/g" "$ZEPPELIN_CONF_DIR/shiro.ini"
printf "done.\n"

printf "> Setting up notebook dir ... \n"
sudo rm -rf "$ZEPPELIN_NB_DIR"
sudo ln -s "$BOI_EFS_ZEPPELIN_NB_DIR" "$ZEPPELIN_NB_DIR"
printf "done.\n"

printf "> Starting zeppelin service ... \n"
sudo start zeppelin
printf "done.\n"

printf "<<< Done.\n\n"

#===============================================================================
#    USERS SETUP
#===============================================================================
printf ">>> Setting up users ... \n"

sudo python3 $BOI_DIR/boi-cli.py users sync -dir "$BOI_EFS_USERS_DIR"

printf "<<< Done.\n\n"

