# Modifying assets in cordra.war

A limited number of customisations to the data.e-rihs.io website require modifying source files within the cordra.war file:

- custom window title and favicon.
- logo and customised landing page link in the nav bar.

Note 1: it is possible to modify these source files in `/opt/cordra/cordra-2.5.2/data/webapps-temp/jetty-0.0.0.0.0.0.0.1-8080-cordra.war-_cordra-any-[*].dir/webapp`, but these will be overwritten each time the Cordra service is restarted. Making those modifications within the war file, makes them persistent during stop/start cycles. __However, the modifications will still need to be redone with each upgrade of Cordra!__

## Instructions

Remarks:

- All instructions below are done as __root__ on the Cordra server.
- Make the files in this directory available on the server (scp, git, wget...). In my case, they are uploaded using scp in `/home/kikirpa/webapp`. If different, make sure to change it in the instructions below
- Cordra is installed in `/opt/cordra/cordra-2.5.2`. Adapt to your set-up.

```bash
# Create a backup of the original war file
cp /opt/cordra/cordra-2.5.2/sw/webapps-priority/cordra.war ~/cordra-orig.war

# Merge the files into the war file (in place)
cd /home/kikirpa/webapp
zip /opt/cordra/cordra-2.5.2/sw/webapps-priority/cordra.war index.html
zip /opt/cordra/cordra-2.5.2/sw/webapps-priority/cordra.war img/e-rihs-kb-logo.png
zip /opt/cordra/cordra-2.5.2/sw/webapps-priority/cordra.war img/favicon.png

# Restart Cordra
systemctl restart cordra
```
