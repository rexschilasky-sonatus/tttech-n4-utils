#!/bin/sh

set -e

echo "Creating symlinks for binaries in /usr/bin/"
for bin in /opt/snt/bin/*; do
    if [ -x "$bin" ]; then
        base=$(basename "$bin")
        ln -sf "$bin" "/usr/bin/$base"
        echo "Linked $base → /usr/bin/$base"
    fi
done

echo ""
echo "Copying snt*.service files to /etc/systemd/system/"
cp -v /opt/snt/etc/systemd/system/snt*.service /etc/systemd/system/

echo "Reloading systemd configuration"
systemctl daemon-reload

echo "Enabling all snt*.service units"
systemctl list-unit-files | awk '/^snt.*\.service/ {print $1}' | while read svc; do
    echo "Enabling $svc"
    systemctl enable "$svc"
done

echo ""
echo "Checking status of all snt*.service units"
systemctl list-units --type=service | grep snt || echo "No snt services currently running."

echo ""
echo "All snt services and binaries have been deployed and enabled."
echo "You can now reboot or start the services manually:"
echo "systemctl start <service>"
