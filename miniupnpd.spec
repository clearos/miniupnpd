Summary: MiniUPNPD Lightweight UPNP Daemon
URL: http://miniupnp.free.fr/files/
Name: miniupnpd
Version: 2.0.20180203
Group: System Environment/Daemons
Release: 3%{?dist}
License: See Source
Source0: %{name}-%{version}.tar.gz
Source1: miniupnpd.service
Source2: miniupnpd.conf
#Source3: miniupnpd.sysconfig
Source4: init_clearos.sh
Source5: iptables_removeall_clearos.sh
Source6: 40-miniupnpd
Source7: miniupnpd_clearos.conf

#Patch1: miniupnpd-2.0.20180203-clearos.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: iptables-devel
BuildRequires:  systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: iptables

%description
The MiniUPnP daemon is an UPnP IGD (internet gateway device) which provide NAT
traversal services to any UPnP enabled client on the network.

%prep
%setup -q 
#%patch1 -p1

%build
make -f Makefile.linux config.h
# Enable lease file in config.h
sed -i -e 's/^\/\*#define ENABLE_LEASEFILE.*/#define ENABLE_LEASEFILE/' config.h
make -f Makefile.linux

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make -f Makefile.linux install PREFIX="%{buildroot}"

rm -f %{buildroot}%{_sysconfdir}/init.d/miniupnpd
install -D -m0644 %{SOURCE1} %{buildroot}%{_unitdir}/miniupnpd.service
install -D -m0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/miniupnpd/miniupnpd.conf
#install -D -m0755 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/miniupnpd
install -D -m0755 %{SOURCE4} %{buildroot}%{_sysconfdir}/miniupnpd/init_clearos.sh
install -D -m0755 %{SOURCE5} %{buildroot}%{_sysconfdir}/miniupnpd/iptables_removeall_clearos.sh
install -D -m0755 %{SOURCE6} %{buildroot}%{_sysconfdir}/clearos/firewall.d/40-miniupnpd
install -D -m0755 %{SOURCE7} %{buildroot}%{_sysconfdir}/miniupnpd/miniupnpd_clearos.conf
install -d -D -m0755 %{buildroot}/var/lib/miniupnpd

%post
%systemd_post miniupnpd.service

%preun
%systemd_preun miniupnpd.service

%postun
%systemd_postun_with_restart miniupnpd.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/miniupnpd/miniupnpd.conf
#%config(noreplace) %{_sysconfdir}/sysconfig/miniupnpd
%{_sysconfdir}/miniupnpd/*sh
%{_mandir}/man8/miniupnpd.*
%{_sbindir}/miniupnpd
%{_unitdir}/%{name}.service
/var/lib/miniupnpd
%{_sysconfdir}/clearos/firewall.d/40-miniupnpd
%config(noreplace) %{_sysconfdir}/miniupnpd/miniupnpd_clearos.conf

%changelog
* Wed Feb 23 2018 Nick Howitt <nhowitt@clearcenter.com> - 2.0.20180203-3
- Add 40-miniupnpd to restart service on firewall restart

* Wed Feb 21 2018 Nick Howitt <nhowitt@clearcenter.com> - 2.0.20180203-1
- Add 40-miniupnpd to restart service on firewall restart

* Sat Feb 10 2018 Nick Howitt <nhowitt@clearcenter.com> - 2.0.20180203-1
- Updated miniupnpd to 2.0.20180203-1
- Remove dependency on firewall.lua
- Change auto-configuration of interfaces

* Fri Jun 26 2015 Peter Baldwin <peter@egloo.ca> - 1.9.20150609-1
- Updated for ClearOS 7, systemd

* Mon Nov 18 2013 ClearFoundation <developer@clearfoundation.com> - 1.6.20120121-6
- Standardized configuration file name
- Migrated to git

* Mon Sep 09 2013 ClearFoundation <developer@clearfoundation.com> - 1.6.20120121-5
- Added patch for ClearOS build

* Fri Apr 27 2012 Tim Burgess <trburgess@gmail.com> - 1.6.20120121-4
- Fix release

* Fri Apr 27 2012 Tim Burgess <trburgess@gmail.com> - 1.6.20120121-3
- Remove dist, vendor tags

* Mon Mar 12 2012 Peter Baldwin <pbaldwin@clearfoundation.com> - 1.6.20120121-2
- Enabled lease file support

* Fri Feb 24 2012 Peter Baldwin <pbaldwin@clearfoundation.com> - 1.6.20120121-1
- Imported into build system

* Thu Mar 10 2011 Tim Burgess <timb80@yahoo.com> - 1.5.20110309
- Update to 1.5.20110309

* Sun Nov 28 2010 Tim Burgess <timb80@yahoo.com> - 1.4.20100921-2
- Amended init script to enumerate all LAN's

* Sat Nov 27 2010 Tim Burgess <timb80@yahoo.com> - 1.4.20100921-1
- First build
