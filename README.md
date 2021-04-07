# COVID Vaccine Appointment Checker

    python3 check.py

Requires:

 * python3.7+
   * requests

This script is configured to check various websites for appointments in the Portland, OR metro area.

When ran, it will check each website. If an availability is found, it will print the name of the store that has an available
appointment. Otherwise, it prints nothing unless an error is encountered.

This script is intended to be run periodically in a cron job. Cron can easily be configured to automatically send you an email
if anything is written to STDOUT/STDERR. This means that, when configured properly, the script will immediately send you an
email informing you that an appointment was found at a particular store.

In order to use it in a different location, you need to change some of the values contained within the script.
For example, the lat/long coordinates found in the walgreens_checker function. That function is also configured to search for
appointments starting on April 19th, as that is when I am eligible for vaccination.
