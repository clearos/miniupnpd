Summary: MiniUPNPD Lightweight UPNP Daemon
URL: http://miniupnp.free.fr/files/
Name: miniupnpd
Version: 1.6.20120121
Group: Network/Other
Release: 6%{?dist}
License: See Source
Source0: %{name}-%{version}.tar.gz
Source1: miniupnpd-init
Source2: miniupnpd.conf
Patch1: miniupnpd-1.6.20120121-clearos.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: iptables-devel
Requires: iptables

%description
The MiniUPnP daemon is an UPnP IGD (internet gateway device)which provide NAT traversal services to any UPnP enabled client on
the network.
See http://www.upnp.org/ for more details on UPnP.

Later, support for the NAT Port Mapping Protocol (NAT-PMP) was added. See information about NAT-PMP here :
http://miniupnp.free.fr/nat-pmp.html

Copyright (c) 2006-2009, Thomas BERNARD
All rights reserved.

%prep
%setup -q 
%patch1 -p1

%build
make -f Makefile.linux config.h
# Enable lease file in config.h
sed -i -e 's/^\/\*#define ENABLE_LEASEFILE.*/#define ENABLE_LEASEFILE/' config.h
make -f Makefile.linux

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make -f Makefile.linux install PREFIX="%{buildroot}"
install -D -m0755 %{SOURCE1} %{buildroot}/etc/init.d/miniupnpd
install -D -m0755 %{SOURCE2} %{buildroot}/etc/miniupnpd/miniupnpd.conf
install -d -D -m0755 %{buildroot}/var/lib/miniupnpd

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add miniupnpd

%preun
/sbin/service miniupnpd stop
/sbin/chkconfig --del miniupnpd

%files
%defattr(-,root,root)
%config(noreplace) /etc/miniupnpd/miniupnpd.conf
/usr/sbin/miniupnpd
/etc/init.d/miniupnpd
/etc/miniupnpd/
/var/lib/miniupnpd

%changelog
* Mon Nov 18 2013 ClearFoundation <developer@clearfoundation.com> - 1.6.20120121-6
- Standardized configuration file name
- Migrated to git

* Mon Sep 09 2013 ClearFoundation <developer@clearfoundation.com> - 1.6.20120121-5
- Added patch for ClearOS build

* Fri Apr 27 2012 Tim Burgess <trburgess@gmail.com> - 1.6.20120121-4
- Fix release

* Fri Apr 27 2012 Tim Burgess <trburgess@gmail.com> - 1.6.20120121-3
- Remove dist, vendor tags

* Mon Mar 11 2012 Peter Baldwin <pbaldwin@clearfoundation.com> - 1.6.20120121-2
- Enabled lease file support

* Fri Feb 23 2012 Peter Baldwin <pbaldwin@clearfoundation.com> - 1.6.20120121-1
- Imported into build system

* Thu Mar 10 2011 Tim Burgess <timb80@yahoo.com> - 1.5.20110309
- Update to 1.5.20110309

* Sun Nov 28 2010 Tim Burgess <timb80@yahoo.com> - 1.4.20100921-2
- Amended init script to enumerate all LAN's

* Sat Nov 27 2010 Tim Burgess <timb80@yahoo.com> - 1.4.20100921-1
- First build
