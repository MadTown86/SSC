# SSC
<p>Learning Exercise : Stock Screener</p>
<p>Date: 10/24/2022</p>
<p>Author: GD</p>
<hr>

<h2>Setup Instructions:</h2>

In order to get this application to function locally from within an IDE.  You will need to update the following items on your local machine:
<p>
<b>1.</b> Root Locations and .ENV file
</p>
<p>
<b>2.</b> API Key Registration and additional Environment Variables
</p>
<p>
<b>3.</b> Create or Associate a MySQL Server
</p>
<hr>

<p>
<h2>1. Root Locations and .ENV file</h2>
<p>(Most likely redundant - will change eventually)</p>
<p>(i). Update environment variables</p>
<p><pre>    a. "LO_ROOT" = location of .ENV file within sscpackage - update this in your local machine environment variables</pre></p>
<p>
<a href="https://imgur.com/ESumFXc"><img src="https://i.imgur.com/ESumFXc.png" title="source: imgur.com" /></a>
</p>
<p><pre>    b. "CORE_DIR_STORE" = path to the ".sscpackage\storage\" folder on your local machine - update this in the .ENV file</pre></p>
</p>

<p><a href="https://imgur.com/H3kY1y3"><img src="https://i.imgur.com/H3kY1y3.png" title="source: imgur.com" /></a></p>
<hr>

<p>
<p><h2>2. API Key Registration and additional Environment Variables</h2></p>

<p><pre>    a. Sign up for a personal free account on <a href='rapidapi.com'>RapidApi.com</a></pre></p> 

<p><pre>    b. Create an 'application' in your rapidapi.com account</pre></p>

<p><a href="https://imgur.com/gOtBpta"><img src="https://i.imgur.com/gOtBpta.png" title="source: imgur.com" /></a></p>

<p><pre>    c. Make note of your securitykey and create environment variable "RAPI_key"</pre></p>

<p><pre>         1. You will have a set number of fetches from YH Finance that you can use for free to test app</pre></p>

<p><a href="https://imgur.com/yHzNjsg"><img src="https://i.imgur.com/yHzNjsg.png" title="source: imgur.com" /></a></p>
</p>

<hr>

<p>

<p><h2>3. Create or Associate a MySQL Server</h2></p>

<p><pre>    a. Create a server with MySQL Workbench - <a href="https://dev.mysql.com/downloads/workbench/">download page</a></pre></p>

<p><pre>        i. Or use other software that can create an appropriate 'host' location for pythons mysql.connector</pre></p>

<p><pre>    b. Create local machine invironment variables for "localhost", "DB_USER", "DB_PASS"</pre></p>

<p><a href="https://imgur.com/fnTQnGc"><img src="https://i.imgur.com/fnTQnGc.png" title="source: imgur.com" /></a></p>

</p>

<hr>

<p><h1>Run Instructions</h1></p>
<p>1. Find and run if '__name__ == "__main__":' section of module 'mainssc.py'</p>

<p><a href="https://imgur.com/226sAIp"><img src="https://i.imgur.com/226sAIp.png" title="source: imgur.com" /></a></p>

<p>2. Click 'browse' and select a file with comma separated ticker symbols</p>

<p><a href="https://imgur.com/VVFswN5"><img src="https://i.imgur.com/VVFswN5.png" title="source: imgur.com" /></a></p>

<p>3. Click 'Submit' button and program should run through list of ticker symbols and final outcome will be stored in local database</p>
<p><a href="https://imgur.com/Ieo616i"><img src="https://i.imgur.com/Ieo616i.png" title="source: imgur.com" /></a></p>

<p><pre>    a. Otherwise click on the 'show db' button on the GUI to check stored values</pre</p>
<p><a href="https://imgur.com/x87dIWu"><img src="https://i.imgur.com/x87dIWu.png" title="source: imgur.com" /></a></p>

<p><h1>Author Comments</h1></p>
<p>1. This is a work in progress.  As of 10/24/22 the program works with the current API's, so long as the YH Finance API remains constant, it should work</p>
<p>2. Please create 'issues' if you find that there are core issues that need to be resolves or if things need to be corrected</p>
<p>3. To alter the way stocks are graded, you will need to alter the awardsystemssc.py or the 'grade_...' modules</p>
