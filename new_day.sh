set -e

YEAR=$1
DAY=$2

if [ -z "$YEAR" ] || [ -z "$DAY" ]
then
    echo "Usage: new_day.sh <YEAR> <DAY> [--force]"
    echo "Example: new_day.sh 2020 12"
    exit 1
fi

if [ "$3" == "--force" ]
then
    echo "Force is on"
    FORCE="1"
fi


CUR_YEAR=`date +'%Y'`
if ([ "$YEAR" -gt "$CUR_YEAR" ] || [ "$YEAR" -lt "2015" ]) && [ -z "$FORCE" ]
then
    echo "It's not ${YEAR} yet, if you want to create it anyway add '--force'"
    exit 1
fi

if ([ "$DAY" -gt "25" ] || [ "$DAY" -lt "1" ]) && [ -z "$FORCE" ]
then
    echo "Invalid day specified '${DAY}', if you want to create it anyway add '--force'"
    exit 1
fi

echo "Preparing env for AoC ${YEAR} day ${DAY}"

git checkout -b aoc-${YEAR}-day-${DAY}
if [ ! -d "${YEAR}" ]
then
    mkdir "${YEAR}"
fi
mkdir "${YEAR}/${DAY}"
touch "${YEAR}/${DAY}/input.txt"
touch "${YEAR}/${DAY}/solution.py"

echo "You env for AoC ${YEAR} day ${DAY} is ready"
echo "Paste your puzzle input into: '${YEAR}/${DAY}/input.txt'"
echo "Write your solution to the puzzle in:  '${YEAR}/${DAY}/solution.py'"
echo "To run your solution execute: 'python ${YEAR}/${DAY}/solution.py'"
echo "Time is ticking.... Goodluck!"
