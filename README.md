# Schedule-Teachers

This project is about schedule teachers and timetables to classes using cp and or-tools

# Problem 

There are T teachers 1,2,…, T needs to be assigned to teach subjects for classes. There are M subjects 1, 2, …, M

• There are N classes 1, 2,…, N. Each class has 1 list of subjects (take
from 1, 2, …, M). Each class associated with a subject is called a class-subject

• Each subject m has the number of periods d(m)

• Each teacher has a list of subjects that he or she can teach

• Each session is divided into 5 periods

• Need to develop a plan to assign teachers as well as a timetable
(start date/period) for each satisfactory class-subject

• Class-subjects in the same class are not allowed  to overlap

• Classes-subjects assigned to the same teacher are also not allowed overlap

There are 5 school days a week, from Monday to Friday, each day has two sessions in the morning and afternoon

# Input
• Line 1: T (number of teachers), N (number of classes), M (number of subjects)
• Line i+1 (i = 1,…, N):  enumerate the subjects that class i needs to learn (ended by 0)
• The t + N + 1 line (t = 1,2,.., T): list the subjects that the teacher t can teach (ends with 0)
• Nth line + T + 2: write d(m) as the number of periods of subject m (m = 1,…, M)
