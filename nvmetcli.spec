Name:           nvmetcli
License:        Apache License 2.0
Group:          Applications/System
Summary:        An adminstration shell for NVMe storage targets
Version:        0.6
Release:        1%{?dist}
URL:            ftp://ftp.infradead.org/pub/nvmetcli/
Source:         ftp://ftp.infradead.org/pub/nvmetcli/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel python-setuptools systemd-units asciidoc xmlto
Requires:       python-configshell python-kmod
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This package contains the command line interface to the NVMe over Fabrics
nvmet in the Linux kernel.  It allows configuring the nvmet interactively
as well as saving / restoring the configuration to / from a json file.

%prep
%setup -q

%build
%{__python} setup.py build
cd Documentation
make
gzip --stdout nvmetcli.8 > nvmetcli.8.gz

%install
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/nvmet
#install -m 755 nvmetcli %{buildroot}/usr/sbin/nvmetcli
install -m 644 nvmet.service %{buildroot}%{_unitdir}/nvmet.service
mkdir -p %{buildroot}%{_mandir}/man8/
install -m 644 Documentation/nvmetcli.8.gz %{buildroot}%{_mandir}/man8/

%post
%systemd_post nvmet.service

%preun
%systemd_preun nvmet.service

%postun
%systemd_postun_with_restart nvmet.service

%files
%{python_sitelib}/*
%dir %{_sysconfdir}/nvmet
%{_sbindir}/nvmetcli
%{_unitdir}/nvmet.service
%doc COPYING README
%{_mandir}/man8/nvmetcli.8.gz

%changelog
* Tue Jul 31 2018 Maurizio Lombardi <mlombard@redhat.com> - 0.6-1
- Update for new upstream release

* Tue Nov 14 2017 Maurizio Lombardi <mlombard@redhat.com> - 0.5-1
- Update for new upstream release

* Tue May 9 2017 Andy Grover <agrover@redhat.com> - 0.4-1
- Update for new upstream release
- Remove fix-setup.patch

* Tue Feb 21 2017 Andy Grover <agrover@redhat.com> - 0.3-1
- Update for new upstream release

* Wed Oct 12 2016 Andy Grover <agrover@redhat.com> - 0.2-1
- Initial packaging
