Name:           lldpad
Version:        0.9.38
Release:        3%{?dist}
Summary:        Intel LLDP Agent

Group:          System Environment/Daemons
License:        GPLv2
URL:            http://e1000.sourceforge.net
Source0:		http://downloads.sourceforge.net/project/e1000/DCB%20Tools/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch0:         lldpad-0.9.7-init.patch
Patch1:         lldpad-0.9.19-init-lsb.patch
Patch2:         lldpad-0.9.29-make.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:         kernel >= 2.6.32
BuildRequires:    libconfig-devel >= 1.3.2 kernel-headers >= 2.6.32
Requires(post):   chkconfig
Requires(preun):  chkconfig initscripts
Requires(postun): initscripts
Provides:         dcbd = %{version}-%{release}
Obsoletes:        dcbd < 0.9.26

%description
This package contains the Linux user space daemon and configuration tool for
Intel LLDP Agent with Enhanced Ethernet support for the Data Center.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       dcbd-devel = %{version}-%{release}
Obsoletes:      dcbd-devel < 0.9.26

%description    devel
The %{name}-devel package contains header files for developing applications
that use %{name}.

%prep
%setup -q
%patch0 -p1 -b .init
%patch1 -p1 -b .init-lsb
%patch2 -p1 -b .make


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_initddir}
mv $RPM_BUILD_ROOT/etc/init.d/%{name} $RPM_BUILD_ROOT%{_initddir}
rm -rf $RPM_BUILD_ROOT/etc/init.d
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/dcbd.8

%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
        /sbin/service %{name} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ]; then
        /sbin/service %{name} condrestart > /dev/null  2>&1 || :
fi

%post devel
## provide legacy support for apps that use the old dcbd interface.
test -e %{_includedir}/dcbd || `ln -T -s %{_includedir}/lldpad %{_includedir}/dcbd`
test -e %{_includedir}/dcbd/clif_cmds.h || `ln -T -s %{_includedir}/lldpad/lldp_dcbx_cmds.h %{_includedir}/dcbd/clif_cmds.h`

%preun devel
test -e %{_includedir}/dcbd/clif_cmds.h && `rm -f %{_includedir}/dcbd/clif_cmds.h`
test -e %{_includedir}/dcbd && `rm -f %{_includedir}/dcbd`


%files
%defattr(-,root,root,-)
%doc COPYING README ChangeLog
%{_sbindir}/*
%dir %{_sharedstatedir}/%{name}
%{_initddir}/%{name}
%{_mandir}/man8/*

%files devel
%defattr(-,root,root,-)
%doc COPYING
%doc README
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Jul 30 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.38-3
- another version of previous fix

* Fri Jul 30 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.38-2
- lldpad is starting on all runlevels by default (#619605)

* Tue Jun 22 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.38-1
- rebased to 0.9.38 (various enhancements and bugfixes, see 
  lldpad-0.9.38-relnotes.txt on http://e1000.sf.net for complete list)

* Thu Mar 25 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.32-2
- added Provides and Obsoletes tags to devel subpackage

* Tue Mar 23 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.32-1
- rebased to 0.9.32 (various enhancements and bugfixes, see 
  lldpad-0.9.32-relnotes.txt on http://e1000.sf.net for complete list)

* Mon Mar 15 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.29-2
- minor correction of init script (LSB compliance was broken
  by renaming of the package)

* Mon Mar 15 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.29-1
- update to 0.9.29 for compatibility with fcoe-utils

* Fri Feb 26 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.26-2
- updated URL of upstream source tarball

* Thu Feb 25 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.26-1
- rebased to 0.9.26
- package renamed to lldpad
- enahanced functionality (LLDP supported as well as DCBX)

* Fri Nov 13 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.19-2
- init script patch adding LSB compliance

* Thu Oct 08 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.19-1
- update to new upstream version

* Mon Oct 05 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.15-5
- replaced the last patch, which was not fully functional, with
  the new one

* Wed Sep 09 2009 Karsten Hopp <karsten@redhat.com> 0.9.15-4
- buildrequire libconfig-devel >= 1.3.2, it doesn't build with 1.3.1 due to
  the different config_lookup_string api

* Thu Aug 20 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.15-3
- update of config_lookup_string() function calls

* Thu Aug 20 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.15-2
- rebuild in order to match new libconfig

* Mon Aug 17 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.15-1
- rebase to 0.9.15

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 20 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.7-4
- updated scriptlets in spec file to follow the rules

* Wed Mar 11 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.7-3
- added devel files again to support fcoe-utils package
- added kernel >= 2.6.29 to Requires, deleted dcbnl.h, since it is
  aviable in kernel 2.6.29-rc7
- changed config dir from /etc/sysconfig/dcbd to /etc/dcbd
- updated init script: added mandatory Short description tag,
  deleted default runlevels, which should start the script

* Tue Mar 10 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.7-2
- added patch to enable usage of libconfig shared in system
- removed devel part of package

* Mon Mar 2 2009 Chris Leech <christopher.leech@intel.com> - 0.9.7-1
- Updated to 0.9.7
- Added a private copy of dcbnl.h until kernel-headers includes it.
  Export patch is making it's way to the upstream kernel via net-2.6,
  expected in 2.6.29-rc7

* Thu Feb 26 2009 Chris Leech <christopher.leech@intel.com> - 0.9.5-1
- initial RPM packaging

