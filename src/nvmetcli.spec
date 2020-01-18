Name:           nvmetcli
License:        Apache License 2.0
Group:          Applications/System
Summary:        Command line interface for the kernel NVMe nvmet
Version: 0.4
Release:        1%{?dist}
URL:		http://git.infradead.org/users/hch/nvmetcli.git
Source:         nvmetcli-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-rpmroot
BuildArch:      noarch
BuildRequires:  python-devel python-setuptools systemd-units
Requires:	python-configshell python-kmod python-six
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This package contains the command line interface to the NVMe over Fabrics
nvmet in the Linux kernel.  It allows configuring the nvmet interactively
as well as saving / restoring the configuration to / from a json file.

%prep
%setup -q -n nvmetcli-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root=%{buildroot} --prefix=usr
mkdir -p %{buildroot}%{_sysconfdir}/nvmet
mkdir -p %{buildroot}%{_unitdir}
install -m 644 nvmet.service %{buildroot}%{_unitdir}/nvmet.service

%clean
rm -rf %{buildroot}

%post
%systemd_post nvmet.service

%preun
%systemd_preun nvmet.service

%postun
%systemd_postun_with_restart nvmet.service

%files
%defattr(-,root,root,-)
%{python_sitelib}
%dir %{_sysconfdir}/nvmet
/usr/sbin/nvmetcli
%{_unitdir}/nvmet.service
%doc COPYING README

%changelog
* Fri Apr 21 2017 Christoph Hellwig <hch@lst.de> 0.4-1
  - Generated from git commit 5078207f0294ebeec5fc6e963eefa2de7d2ce3da.
