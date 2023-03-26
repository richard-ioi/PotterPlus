#!/bin/bash
echo -e "Subject:$2\n$3" | msmtp $1
exit 0