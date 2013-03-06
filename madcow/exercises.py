import datetime
import emailclient
import re
import sqlite3
import sys

gmail_user, gmail_pwd, phone, db = sys.argv[1:5]

conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Squat == 1, Bench Press == 2, Row == 3, Military Press == 4, Deadlift == 5:
routine = { 0: {'Sets': [1,2,3,4,5], 'Exercises': [1,2,3], 'Last': []},
            2: {'Sets': [1,2,3,4], 'Exercises': [1,4,5], 'Last': [4,5]},
            4: {'Sets': [1,2,3,4,5.2,3], 'Exercises': [1,2,3], 'Last': [1,2,3]} }

def scrub(sql):
    return ''.join( chr for chr in sql if chr.isalnum() )

def preparedateinsert(inputdatetime):
    year = inputdatetime.year
    month = inputdatetime.month
    day = inputdatetime.day
    return "{0}{1}{2}{3}{4}".format(year, "0" if month<10 else "", month, "0" if day<10 else "", day)

def convert_to_datetime(datestring):
    previousYear = int(datestring[0:4])
    previousMonth = int(datestring[4:6].lstrip("0"))
    previousDay = int(datestring[6:].lstrip("0"))
    return datetime.date(previousYear, previousMonth, previousDay).weekday()

def parse_text_email_for_date(text_email):
    try:
        return re.search('201[3-9][0-1][0-9][0-3][0-9]', text_email.upper()).group(0)
    except AttributeError:
        return None # set up a text/email for an error message

def parse_text_email_for_success(exercise, text_email):
    letter1_upper = exercise[0].upper()
    formatted_success_regex = '(?<={0})[Y|N]'.format(letter1_upper)
    success_response = re.search(formatted_success_regex, text_email.upper()).group(0)
    return {'Y': 1, 'N': 0}[success_response]

def get_five_rep_max(exercise_id, c):
    weight_reps = c.execute("SELECT * FROM Exercises WHERE ExerciseID=?", [exercise_id]).fetchone()
    weight, reps = weight_reps['MaxWeight'], weight_reps['Reps']
    one_rep_max = weight/(1.0278-(.0278*reps))
    five_rep_max = weight/(1.0278-(.0278*reps))*(1.0278-(.0278*5))
    return five_rep_max

def check_if_table_exists(table_name, c):
    try:
        return c.execute("SELECT * FROM sqlite_master WHERE tbl_name=?", [table_name]).fetchone()
    except sqlite3.OperationalError:
        return None

def check_all_tables(c):
    if not check_if_table_exists('Exercises', c):
        createexercisetable(c)
        insertintoexercisetable(c)
    if not check_if_table_exists('ExerciseHx', c):
        createhxtable(c)
        for exercise_id in routine[4]['Last']+routine[2]['Last']:
            insertintohxtable(exercise_id, 0, 0, c)

def createexercisetable(c):
    c.execute('CREATE TABLE Exercises (ExerciseID INTEGER PRIMARY KEY'
                                     ',ExerciseName varchar(50)'
                                     ',MaxWeight int'
                                     ',Reps int'
                                     ',Failures int)')
    
def insertintoexercisetable(c):
    c.execute("""INSERT INTO Exercises
                 SELECT 1 AS ExerciseID, 'Squat' AS ExerciseName, 135 AS MaxWeight, 5 AS Reps, 0 AS Failures UNION
                 SELECT 2 AS ExerciseID, 'Bench' AS ExerciseName, 125 AS MaxWeight, 5 AS Reps, 0 AS Failures UNION
                 SELECT 3 AS ExerciseID, 'Row'   AS ExerciseName, 105 AS MaxWeight, 5 AS Reps, 0 AS Failures UNION
                 SELECT 4 AS ExerciseID, 'MP'    AS ExerciseName, 85  AS MaxWeight, 5 AS Reps, 0 AS Failures UNION
                 SELECT 5 AS ExerciseID, 'DL'    AS ExerciseName, 165 AS MaxWeight, 5 AS Reps, 0 AS Failures""")

def createhxtable(c):
    c.execute('CREATE TABLE ExerciseHx (ExerciseHxID INTEGER PRIMARY KEY'
                                      ',ExerciseID int'
                                      ',Week int'
                                      ',Success int'
                                      ',MaxWeight int'
                                      ',AuditDate char(8))')

def insertintohxtable(exercise_id, week, success, c, maxweight=0, date='20130301'):
    c.execute("""INSERT INTO ExerciseHx (ExerciseID, Week, Success, MaxWeight, AuditDate)
                 VALUES (?, ?, ?, ?, ?)""", [exercise_id, week, success, maxweight, date])

def getmostrecentlift(exercise_id, c):
    return c.execute("""SELECT *
                        FROM ExerciseHx
                        INNER JOIN
                            (SELECT MAX(ExerciseHxID) AS MostRecent
                             FROM ExerciseHx
                             WHERE ExerciseID = ?) X 
                        ON X.MostRecent = ExerciseHx.ExerciseHxID""", [exercise_id]).fetchone()

def get_top_set(current_max, week):
    try:
        week = int(week)
        if week < 4:
            return current_max*(.975**(4-week))
        elif week == 4:
            return current_max
        elif week > 4:
            return current_max*(1.025**(week-4))
    except ValueError:
        print "You have bad data and don't have good exception handling set up yet!"
        raise
    
def getExercisePlan(routine, day_of_the_week, c):
    exerciseOutput = {}

    current_workout = routine[day_of_the_week]
    current_exercises = current_workout['Exercises']
    current_sets = current_workout['Sets']

    for exercise_id in current_exercises:
        exercise = c.execute("SELECT * FROM Exercises WHERE ExerciseID=?", [exercise_id]).fetchone()['ExerciseName']
        exerciseOutput[(exercise_id, exercise)] = "{0}: ".format(exercise)

        five_rep_max = get_five_rep_max(exercise_id, c)
        recent_exercise_hx = getmostrecentlift(exercise_id, c)
        top_set = get_top_set(five_rep_max, recent_exercise_hx['Week']+recent_exercise_hx['Success'])

        for set_foo in current_sets:
            set_number = current_sets.index(set_foo)+1
            if day_of_the_week == 2 and exercise == 'Squat' and set_number == 4:
                set_foo = 3
            exerciseOutput[(exercise_id, exercise)] += "{0} ".format(int(round(top_set*.125*(3+set_foo))))
        exerciseOutput[(exercise_id, exercise)] += "\n"
    return exerciseOutput

def makerecordofpreviousworkout(message, routine, c):
    input_date_string = parse_text_email_for_date(message)
    input_date_string_weekday = convert_to_datetime(input_date_string)

    for exercise_id in routine[input_date_string_weekday]['Exercises']:
        exercise_record = c.execute("SELECT * FROM Exercises WHERE ExerciseID=?", [exercise_id]).fetchone()
        exercise = exercise_record['ExerciseName']
        success = parse_text_email_for_success(exercise, message)
        max_in_cycle = exercise_record['MaxWeight']

        previous_lift_hx = getmostrecentlift(exercise_id, c)
        week = previous_lift_hx['Week']
        exercise_id = previous_lift_hx['ExerciseID']

        if exercise_id in routine[input_date_string_weekday]['Last'] and success == 1:
            week += 1
        elif success == 0:
            updated_max_failures = exercise_record['Failures']+1
            c.execute("UPDATE Exercises SET Failures=? WHERE ExerciseID=?", [updated_max_failures, exercise_id])
            check_max_failures(exercise_id, updated_max_failures, c)
        insertintohxtable(exercise_id, week, success, c, max_in_cycle, input_date_string)

def check_max_failures(exercise_id, failures, c):
    if failures > 1:
        most_recent_success = c.execute("""SELECT *
                                           FROM ExerciseHx
                                           INNER JOIN
                                               (SELECT MAX(ExerciseHxID) AS MostRecent
                                                FROM ExerciseHx
                                                WHERE ExerciseID = ?
                                                AND Success = 1) X 
                                           ON X.MostRecent = ExerciseHx.ExerciseHxID""", [exercise_id]).fetchone()
        new_max = get_top_set(most_recent_success['MaxWeight'], most_recent_success['Week'])
        c.execute("UPDATE Exercises SET MaxWeight=?, Failures=0 WHERE ExerciseID=?", [new_max, exercise_id])

def main(c):
    day_of_the_week = datetime.datetime.today().weekday()
    # day_of_the_week = 0
    if day_of_the_week not in [0,2,4]:
        day_off_message = "Today is your day off!"
        emailclient.send(gmail_user+"@gmail.com", gmail_pwd, phone, day_off_message)
        return ''

    check_all_tables(c)
    message_received = emailclient.receive(gmail_user, gmail_pwd, phone)
    makerecordofpreviousworkout(message_received, routine, c)
    workout_string = ""
    exerciseOutput = getExercisePlan(routine, day_of_the_week, c)

    for exercise, list_of_weights in sorted(exerciseOutput.iteritems()):
        workout_string += list_of_weights
    
    emailclient.send(gmail_user+"@gmail.com", gmail_pwd, phone, workout_string)
    conn.commit()
    c.close()
    conn.close()

if __name__ == "__main__":
    main(c)