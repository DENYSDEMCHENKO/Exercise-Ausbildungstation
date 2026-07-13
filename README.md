# Exercise-Ausbildungstation


Recruiting Exercise

Please download the Apache access logfile from here: ftp://ita.ee.lbl.gov/traces/NASA_access_log_Jul95.gz

This file contains one month's worth of all HTTP requests to the NASA Kennedy Space Center WWW server in Florida.

Format

The logs are an ASCII file with one line per request, with the following columns:

1. host making the request. A hostname when possible, otherwise the Internet address if the name could not be looked up.
2. timestamp in the format "DAY/MONTH/YEAR:HH:MM:SS -0400", where DAY is the day of the month, MONTH is the name of the
   month and YEAR is the year, HH:MM:SS is the time of day using a 24-hour clock. The timezone is -0400.
3. request given in quotes.
4. HTTP reply code.
5. bytes in the reply.

Measurement

The first log was collected from 00:00:00 July 1, 1995 through 23:59:59 July 31, 1995, a total of 31 days.

Tasks

(GENERAL)<br>
Please work with one or multiple feature branches in your git repository.
Push all relevant changes in your project into the github repository.
Please also create a pull-request to the main branch for any meaningful increment for which this might make sense.

(1) Basic parsing<br>
Create a log parser program in either Bash, Perl, Python, Ruby or Golang to extract the following information from the logfile:

1. How many requests per Host/IP are in the logfile in total? Please output the Top10 sorted descending
2. (Optional) How many HTTP status codes 2xx, 3xx, 4xx, 5xx have there been per day from 01/07 until 07/07?

(2) Extension<br>
Extend the program to get the current CPU and RAM usage from the local host
(To get some dynamic values - used later for monitoring)

(3) Output<br>
Extend the program to output the values/metrics in the following (open-metrics / prometheus) format:
Example:

# HELP http_requests_total The total number of HTTP requests.
# TYPE http_requests_total gauge
http_requests_total{code="2xx"} 1027
http_requests_total{code="4xx"}    3
1. Create output of the values every 15 seconds in /var/log
2. Ensure the implemented functionality is covered by unit tests

(4) HTTP and Docker<br>
Adapt the application, so it is able to run inside a Docker container and exposes the metrics via HTTP on Port 8000 instead /var/log

(5) Prometheus<br>
Install a prometheus server on the local machine https://prometheus.io/docs/introduction/first_steps/
Hint: You may use Docker

(6) Scraping<br>
Configure the scrape_config of the prometheus to "scrape" the metrics from task (5) in order to deliver them into Prometheus
