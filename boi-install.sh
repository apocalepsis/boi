#!/bin/bash

BOI_DIR="/opt/boi"
BOI_3P_DIR="$BOI_DIR/3p"

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
                $ARG_VALUE_NEW_SETUP=1
                printf "Argument <%s>,Value <%s>\n" "new" "$ARG_KEY_NEW_SETUP" "$ARG_VALUE_NEW_SETUP"
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
printf ">>> Loading properties ...\n"

printf "> Setting up boi dir <%s>" "$BOI_DIR"
mkdir -p $BOI_DIR

printf "> Downloading <3p> dir from <%s> to <%s>" "$ARG_VALUE_S3_URI" "$BOI_3P_DIR"
mkdir -p "$BOI_3P_DIR"
aws s3 cp "$ARG_VALUE_S3_URI/3p/" "$BOI_3P_DIR"

printf "<<< Done.\n\n"