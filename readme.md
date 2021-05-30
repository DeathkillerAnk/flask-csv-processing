### Flask app where you can send csv file to do following
1. The file contains a type column using that you need to filter out on the basis of paid and
free apps. Create 2 child datasets(one for each paid and free) from the input data file.
2. Filter out on the basis of content rating. Create child datasets(one for each content
ratings) from the input data file.
3. Add a new column in the parent dataset with the name “Rating Roundoff ”. This column
should have rounded-off values of the corresponding ratings. Ratings should be
rounded-off to the nearest natural number.

#### To run

0. install pandas, zipfile

1. run   `flask app`

2. open `http://localhost:5000/` & upload " appdatatask.csv" file

3. open `http://localhost:5000/type_split/appdatatask.csv` to perform 1st task.

4. open `http://localhost:5000/filter/appdatatask.csv` to perform 2nd task

5. open `http://localhost:5000/roundoff/appdatatask.csv` to perform 3rd task

