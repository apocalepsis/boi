#!/bin/bash

NEW_SETUP=0

REPO_S3_URI=""

#===============================================================================
#    ARGUMENTS PARSING
#===============================================================================
printf ">>> Validating arguments ...\n"

if [[ $# > 0 ]]; then

    while [[ "$1" != "" ]]; do

        case "$1" in
            "-repo-s3uri" )
                shift
                BOI_REPO_S3_BUCKET_NAME="$1"
                printf "Argument <%s>,Value <%s>\n" "s3repo" $REPO_S3_URI
                ;;
            "-new" )
                NEW_SETUP=1
                printf "Argument <%s>,Value <%s>\n" "new" $NEW_SETUP
                ;;
            * )
                printf "[ERROR] Invalid argument <%s>\n" "$1"
                exit 1
                ;;
        esac
        
        shift
    
    done

fi

printf "<<< Done.\n\n"
