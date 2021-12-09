#! /bin/bash

function replace_readme_str() {
  #statements
  local file=$1/README.md
  local old=$2
  local new=$3

  perl -pi.bak -0 -e "s/${old}/${new}/" $file
  rm -f $1/README.md.bak
}

replace_readme_str $1 "failsafe" "failsafe-findbugs"

replace_readme_str $1 "surefire" "surefire-findbugs"

replace_readme_str $1 "spock" "spock-findbugs"

replace_readme_str $1 "- maven" "- maven\n\t- findbugs"

replace_readme_str $1 "# Description\n" "# Description\nAnalyze source code for potential bugs.\n"

replace_readme_str $1 "\n## To stop" "- findbugs report at bin\/target\/findbugs\n\n## To stop"
