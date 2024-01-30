Sync to device
==============

To make the network devices synchronize their configuration to the latest version generated
by CNaaS the device_syncto API call is used. This will push the latest configuration to
the devices you select.

You can choose to either synchronize all devices, or just synchronize a specific type of device,
or synchronize just a specific hostname.

Example API call:

::

   curl https://hostname/api/v1.0/device_syncto -d '{"hostname": "eosdist", "dry_run": true}'
   -X POST -H "Content-Type: application/json"

This will start a "dry run" synchronization job for the device called "eosdist". A dry run job
will send the newly generated configuration to the device and then generate a diff to see
what lines would have been changed. The response from this API call is a reference to a job id
that you can poll using the job API. This is to make sure that long running jobs does not block
the client. If you synchronize many devices at the same time the job can take a very long time
and the client might time out otherwise.

Example response:

::

  {
    "status": "success",
    "data": "Scheduled job to synchronize eosdist",
    "job_id": "5d5aa787ba050d5fd085f1ce"
  }

The status success in this case only means that the job was scheduled successfully, but
you have to poll the job API to see that result of what was done, the job itself might still
fail.

Configuration changes can be made in a way that requires a separate confirm call since version 1.5.
If the change can not be confirmed because the device is not unreachable for example, the device
will roll back the configuration. Before version 1.5 this concept was not supported, but from this
version it's supported and enabled by default using mode 1.

.. _commit_confirm_modes:

**Commit confirm modes:**

 - 0 = No confirm commit (default up to version 1.4)
 - 1 = Commit is immediately confirmed for each device when that device is configured
   (default from version 1.5)
 - 2 = Commit is confirmed after all devices in the job has been configured, but only if all were
   successful. This mode is only supported for EOS and JunOS so far, and only supported for small
   number of devices per commit (max 50). If mode 2 is specified and an unsupported device is
   selected that device will use mode 1 instead.

Commit confirm mode can be specified in the configuration file, but it's also possible to override
that setting for a specific job using the API argument confirm_mode (see below).

**Arguments:**

 - hostname: Optional, the hostname of a device
 - device_type: Optional, a device type (access, dist or core)
 - group: Optional, a device group. A group can contain multiple devices.
 - all: Optional, bool. Synchronize all devices (that are not already in sync, see resync option)
 - dry_run: Dry run does not commit any configuration to the device. Boolean, defaults to true.
 - force: If a device configuration has been changed outside of CNaaS the configuration hash
   will differ from the last known hash in the database and this will normally make CNaaS
   abort. If you want to override any changes made outside of CNaaS and replace them with the
   latest configuration from CNaaS you can set this flag to true. Boolean, defaults to false.
 - auto_push: If you specify a single device by hostname and do a dry_run, setting this option
   will cause CNaaS to automatically push the configuration to committed/live state after
   doing the dry run if the change impact score (see :ref:`change_impact_score`) is very low.
 - resync: By default devices that are marked as synchronized in the database will not be
   re-synchronized, if you specify this option as true then all devices will be checked.
   This option does not affect syncto jobs with a specified hostname, when you select only
   a single device via hostname it's always re-synchronized. Defaults to false.
 - comment: Optionally add a comment that is saved in the job log.
   This should be a string with max 255 characters.
 - ticket_ref: Optionally reference a service ticket associated with this job.
   This should be a string with max 32 characters.
 - confirm_mode: Optionally override the default commit confirm mode (see above) for this job.
   Must be an integer 0, 1 or 2 if specified.

If neither hostname or device_type is specified all devices that needs to be sycnhronized
will be selected.

Sync history
------------

When an API call causes a device to become unsynchronized a synchronization event is created
in the synchistory log. You can query or manually add events from this history using the API.

Get synchistory events:

::

   curl https://hostname/api/v1.0/device_synchistory?hostname=eosaccess

Example output:

::

   {
     "status": "success",
     "data": {
       "hostnames": {
         "eosaccess": [
           {
             "cause": "refresh_settings",
             "timestamp": 1688458956.684019,
             "by": "indy",
             "job_id": 123
           }
         ]
       }
     }
   }

If the query parameter "hostname" is left out the API will return events for
all devices.

"cause" is a text string reference to the thing that caused the device to become
unsynchronized. For more details on events see :ref:`sync_status_tutorial`.
"timestamp" is a floating point number representing the seconds since Unix epoch (UTC).
"by" is string referring to what user triggered the event. "job_id" is an integer
referring to a job if this event was triggered by a job, or otherwise it's null.

Manually adding a synchistory event:

::

   curl https://hostname/api/v1.0/device_synchistory -d '{"hostname": "eosaccess", "cause": "oob", "by": "indy"}'
   -X POST -H "Content-Type: application/json"

The "time" paramater can optionally be specified as a floating point number of seconds
since Unix epoch (UTC). If not provided the current time will be used.
