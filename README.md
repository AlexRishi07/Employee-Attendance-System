# Employee Attendance System

**Project No.:** 14  
**Project Title:** Employee Attendance System  
**Language:** Python 3  
**Concepts:** Dictionaries, Lists, Conditions, Functions, File Handling

## Project objective
A console application to add employees, mark daily attendance as Present, Absent or Leave, and view an attendance report for each employee. Data is saved in `attendance.txt` and loaded automatically when the program starts.

## Features
- Employee IDs are generated sequentially, beginning with `E101`.
- Employee data is stored as dictionaries (`id`, `name`, `records`) inside a list.
- Attendance status codes: `P` = Present, `A` = Absent, `L` = Leave.
- Dates are validated using the `YYYY-MM-DD` format and real calendar dates.
- Duplicate attendance for the same employee and date is blocked.
- Attendance percentage = Present days / Marked days × 100.
- Data is saved after each successful add or attendance mark.

## Run
Python 3 is required. No third-party packages are needed.

```bash
python one.py
```

Run the program from the project directory so it can read and write `attendance.txt`.

## Menu
1. Add Employee
2. Mark Attendance
3. View Attendance Report
4. Exit

## Test cases
The four test cases in the assignment should be performed in order using the same `attendance.txt` file.

### Test Case 1 – Normal input
Choose option 1 and enter `Aman`.
Expected: `Employee added: E101 | Aman`

### Test Case 2 – Boundary/minimum input
Choose option 3 and enter `E101` before marking any attendance.
Expected:
```text
Aman: Present0 | Absent0 | Leave0
Attendance: 0.00% (no records)
```

### Test Case 3 – Invalid input
- Option 2, employee `E999`: reports employee not found.
- Option 2, employee `E101`, date `2026-13-45`: reports invalid date.
- Option 2, employee `E101`, date `2026-08-01`, status `X`: reports invalid status.

### Test Case 4 – Different valid scenario
For `E101`, mark:
- `2026-08-01`, status `P`
- `2026-08-02`, status `P`
- `2026-08-03`, status `A`
- `2026-08-04`, status `L`
Then try to mark `2026-08-02` again. The program blocks the duplicate.
Expected report:
```text
Aman: Present2 | Absent1 | Leave1
Attendance: 50.00%
```

## Data file
`attendance.txt` contains JSON-formatted text. This keeps the required filename while making it straightforward to load and save the employee list safely. Do not delete this file between test cases; the assignment specifies that tests run on the same records.
