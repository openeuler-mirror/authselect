Name:          authselect
Version:       1.2.4
Release:       5
Summary:       A tool to select system authentication and identity sources from a list of supported profiles
License:       GPLv3+
URL:           https://github.com/authselect/authselect
Source0:       https://github.com/authselect/authselect/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:        authselect-revert-remove-authselect-compat-package.patch

BuildRequires: autoconf gettext-devel automake libtool popt-devel libcmocka-devel
BuildRequires: m4 gcc pkgconfig pkgconfig(popt) po4a asciidoc python3-devel
BuildRequires: libselinux-devel
Requires:      grep sed systemd gawk coreutils findutils pam >= 1.3.1
Obsoletes:     authselect-libs
Provides:      authselect-libs

%description
Authselect is designed to be a replacement for authconfig (which is the default tool for this 
job on Fedora and RHEL based systems) but it takes a different approach to configure the system. 
Instead of letting the administrator build the PAM stack with a tool (which may potentially 
end up with a broken configuration), it would ship several tested stacks (profiles) that solve 
a use-case and are well tested and supported. At the same time, some obsolete features of 
authconfig would not be supported by authselect.

This package contains commands for selecting system identity and authentication sources, and
common library files for the authselect tool.

Authselect will replace %{_sbindir}/authconfig with a tool that will translate some of the 
authconfig calls into authselect calls. It provides only minimum backward compatibility and 
users are encouraged to migrate to authselect completely.

%package_help

%package compat
Summary:       Tool to provide minimum backwards compatibility with authconfig
Obsoletes:     authconfig < 7.0.1-6
Provides:      authconfig
BuildRequires: python3-devel
Requires:      authselect%{?_isa} = %{version}-%{release}
Requires:      sed

%description compat
This package will replace %{_sbindir}/authconfig with a tool that will
translate some of the authconfig calls into authselect calls. It provides
only minimum backward compatibility and users are encouraged to migrate
to authselect completely.

%package devel
Summary:       Development library files and header files for the authselect tool
Requires:      authselect%{?_isa} = %{version}-%{release}

%description devel
This package contains development library files and headers for the authselect tool. This 
package is used to develop a front-end for the authselect library.

%prep
%autosetup -n %{name}-%{version} -p1

%build
autoreconf -ivf
%configure
%make_build

%install
%make_install

%delete_la_and_a

%check
%make_build check

%pre

%preun

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files
%dir %{_sysconfdir}/authselect
%dir %{_sysconfdir}/authselect/custom
%defattr(-,root,root)
%license COPYING
%{_bindir}/authselect
%doc README.md
%{_sysconfdir}/bash_completion.d/*
%{_datadir}/authselect/default/*
%{_datadir}/locale/*
%{_libdir}/libauthselect.so.3*

%files devel
%defattr(-,root,root)
%{_includedir}/authselect.h
%{_libdir}/libauthselect.so
%{_libdir}/pkgconfig/authselect.pc

%files compat
%{_sbindir}/authconfig
%{python3_sitelib}/authselect/

%files help
%defattr(-,root,root)
%{_datadir}/doc/authselect/*
%exclude %{_datadir}/doc/authselect/README.md
%{_mandir}/*

%posttrans compat
sed -i -E '/^\w+=$/d' %{_sysconfdir}/security/pwquality.conf.d/10-authconfig-pwquality.conf &> /dev/null
exit 0

%changelog
* Sun May 15 2022 yixiangzhike <yixiangzhike007@163.com> - 1.2.4-5
- provide default directory /etc/authselect

* Fri Apr 29 2022 yixiangzhike <yixiangzhike007@163.com> - 1.2.4-4
- delete duplicate file README.md from authselect-help

* Mon Mar 21 2022 yixiangzhike <yixiangzhike007@163.com> - 1.2.4-3
- fix change date for version 1.2.4-2 in changelog

* Fri Jan 14 2022 yixiangzhike <yixiangzhike007@163.com> - 1.2.4-2
- revert "remove authselect compat package"

* Tue Nov 30 2021 yixiangzhike <yixiangzhike007@163.com> - 1.2.4-1
- update to 1.2.4

* Mon Jul 19 2021 yixiangzhike <zhangxingliang3@huawei.com> - 1.2.2-3
- Delete unnecessary gdb from BuildRequires

* Thu Mar 25 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 1.2.2-2
- Delete the DLL of an earlier version

* Sat Jan 23 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 1.2.2-1
- update to 1.2.2

* Fri Jul 24 2020 Liquor <lirui130@huawei.com> - 1.2.1-1
- update to 1.2.1

* Tue Jun 02 2020 SimpleUpdate Robot <tc@openeuler.org>
- Update to version 1.1

* Tue Nov 5 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.1-5
- Delete unused lang files

* Mon Sep 30 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.1-4
- Fix conflict of authselect and authconfig

* Tue Sep 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.1-3
- Package init

