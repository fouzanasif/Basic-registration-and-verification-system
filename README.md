<h1>Basic Registration and Verification System</h1>
<h2>Overview</h2>
<p>Developer's Day are FAST NUCES Karachi's flagship events held annually. 
  In 2023, I was entrusted with automating the manual efforts within the registration, verification, management, scheduling, and mailing activities.
This project is built using Python Flask, Google Sheets, and basic HTML, CSS, and JavaScript (JS, JQuery, and AJAX).</p>
<p>The goals of this system are i) <b>TO REGISTER</b>, ii) <b>TO SCHEDULE</b>, iii) <b>TO MAIL</b>, iv) <b>TO MANAGE</b>, and v) <b>TO VERIFY</b> a participant that wishes to participate in Developer's Day:</p>
  <ul>
    <li>To cater PII (Personal Identification Information) in order to contact the participant</li>
    <li>To authenticate user's athenticity using OTPs on user's provided email</li>
    <li>To register a participant (or team) in their desired competition, provided restrictions such as maximum count allowed, maximum number of participants per team, the university semester-wise restrictions imply.</li>
    <li>To provide additional privileges and options for students of FAST NUCES (helping internal affairs of students within their courses)</li>
    <li>To register, send to waiting list (on unavailability of slots - and to be contacted as soon as a seat is vacant), mail accordingly, and schedule the participant at a venue allocated for that competition</li>
    <li>To verify the participants' registrations on the day of the event and allow them to participate accordingly</li>
  </ul>
<p>And many other goals that cannot be listed (as they are subjected to change quickly).</p>

<h2>Project Functionalities</h2>
<ul>
  <li>For all the <b>DATA VERIFICATION, ADDITION, UPDATION, AND DELETION</b> steps, Google Sheets are used using Python</li>
  <li>Each participant is uniquely identified by Email and has attributes => Name, Phone, Email, and Competition Selected</li>
  <li>A participant receives OTP on email (generated using OTP API within main.py)</li>
  <li>OTP is checked and its correctness against the email is verified. OTPs are saved within the "Verified" worksheet of Google Sheet</li>
  <li>If OTP is not verified, invalid_OTP.html is rendered. Else, the selected competition i.e. CSCompetitions.html or EECompetitions.html is rendered</li>
  <li>The institute and max years of education is acquired from the participant to restrict certain competitions based on competition's target participants</li>
  <li>A participant can select a number of offered competitions, can enter number of participants allowed, add a team name, and refer a Brand Ambassador using competitions page</li>
  <li>If the participant does not belong to FAST NUCES, the registration is processed to be successful or is sent to the waiting list</li>
  <li>If the participant belongs to FAST NUCES (and there are seats available for particular competition), the NU-IDs, Section, Batch for every participant is collected.</li>
  <li>All the input elements are strictly bounded to follow a regular expression provided for each input field in pattern (HTML files)</li>
  <li>Repeated student IDs are neglected.</li>
  <li>A participant cannot participant in same competition twice (However this constraint has been removed currently. In this project, you'll check that there are no 2 registrations against same user)</li>
  <li>No 2 entries against same participant number can be made (will be neglected) e.g. if 2nd participant is 19K-0000, you cannot revisit the 2nd participant page and enter another ID 19K-0001</li>
</ul>

<h2>Project Setup</h2>
<h3>Backend - Python</h3>
<h4>Libraries</h4>
<ul>
  <li><b>Flask</b> with CORS policy enabled, request, and response elements, is used to expose API endpoints</li>
  <li><b>smtplib</b>library is used to send mails. You can change the email and password in Utilities.py</li>
  <li><b>qrcode</b>library is used to generate QR Codes. The data added in QrCode can be changed using qrgen(data) function within Utilities.py file</li>
  <li><b>crypto</b>library is used to generate unique hashes for against each participant's email. The data added in QrCode can be changed using qrgen(data) function within Utilities.py file</li>
  <li><b>gspread</b>library is used to connect to Google Sheets. You'll need a credentials.json file from Google Cloud Platform's Google Sheets API (using OAuth). You'll need to give the id of the sheet to open. Refer to servac and excel variables in Utilities.py</li>
</ul>
<h4>Working</h4>
<ul>
  <li>Using HTML form's action attribute, the processed requests are addressed at the start of each API using request.form</li>
  <li>Using JS and AJAX's fetch attribute, the processed requests are addressed at the start of verification API using request.get_json()</li>
  <li>Each request's data is interpreted as a dictionary containing all the input attributes from HTML input fields (where key of the element in dictionary is the name attribute of input field from HTML)</li>
  <li>The communication between the different APIs and HTML pages is done using query parameters (except in the case of Verification where POST requests are used in HTML internally using JS)</li>
  <li>For adding a new record in Google Sheet, wks.update() is called with a DataFrame passed to it</li>
  <li>For adding a field in Google Sheet, wks.update(cell,[[data]]) is called with a cell and data in double square brackets sent to it</li>
</ul>
<h3>Database - Google Sheets</h3>
Google Sheets was used as a middleware to store, retrieve, and perform data related operations.
<h4>Setup and Working</h4>
<ul>
  <li>Your Google Sheet needs to be accessible for "ANYONE WITH THE LINK" in "EDITOR" mode</li>
  <li>The Id of your google sheet is: https://docs.google.com/spreadsheets/d/(this is your id)/edit#gid=1831284774. This Id is provided in Utilities.py to get excel</li>
  <li>The Sheet used as an example in this project contains several worksheets
  <ul>
    <li>OTP - for keeping OTPs against Email</li>  
    <li>Participants - for keeping information only for the team leader</li>
    <li>Verify - for keeping information of teams participating on the event day</li>
    <li>Waiting - for keeping information of teams leaders in waiting list</li>
    <li>University - for keeping information of FAST NUCES participants</li>
  </ul>
  </li>
  <li>To call wks.update(DataFrame), make sure you've passed all the columns that were expected!</li>
  <li><b>Generating a credentials file is very important to use gspread</b>. A tutorial will soon be posted on how to get this file using Google Cloud's Google Sheets API (using OAuth)</li>
</ul>
<h3>FrontEnd - HTML, CSS, JS</h3>
HTML and CSS were used with common elements on every page to render more or less same design with different input fields. Javascript was used to change DOM elements on the page based on selection changes. And JQuery was used to send API calls to the backend.

<h2>Project Deliverables</h2>
<h3>Files and Folders</h3>
<ul>
  <li><b>_registration</b>: This folder contains all the HTML, CSS, and PNG files that are being used within the application</li>
  <li><b>main.py</b>: This Python file contains the main backend APIs used to fulfill different functionalities and control the data flow accross the application</li>
  <li><b>Utilities.py</b>: This Python file contains functions other than APIs that are being used within these APIs for mailing, storing data, or verifying data</li>
  <li><b>globalDeclarations.py</b>: This Python file contains variables used within the utilities and APIs for sending data (that can be reused)</li>
</ul>
<h3>Project Execution</h3>
<ul>
  <li><code>python main.py</code> - Executes the application at port <b>9922</b> (can be changed in main.py)</li>
  <li><code>static = "./_registration" and template = "./_registration"</code> are set to define all the HTML and CSS files only in _registration folder</li>
</ul>


<h2>Project Flaws</h2>
<p>Well, the project has way too many flaws. Being developed on a very short notice, security vulnerabilities, manageability, SOLID principles, and resilience were brutally massacred. Some areas to be addressed within the project are:</p>
<ul>
  <li>Passing values using params is the least preferred approach to communicate between pages and backend as it exposes the data to be manually altered, is available accross pages and network packets, and the params can be misused by bots.</li>
  <li>HTML code has too many redundancies. Each input element has the same styling element. The change, though minimal, has to be done accross many HTML pages/</li>
  <li>Improper coding practices were used in Backend. The APIs are not effectively written, take time, are not session authenticated (thus prone to DDoS attacks)</li>
  <li>The naming conventions, functionality usage, Single Responsibility Principle, Exception handling etc. were not very well handled (but used at some points).</li>
</ul>

<h2>Conclusion</h2>
There's always more to come than what's accomplished. Being my first publicly used app, I acquired the exposure of how to create an app in first place, and learn the mistakes that I have committed while creating the app. Also, I learnt how to align oneself to capture minimal attention to details, and outperform in difficult situations. The later releases for this simple project are yet to come.
