# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?__python2: %global __python2 %__python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

# Use python2 by default
%bcond_without python2
%bcond_with python3

Name: salmon
Version: 1.0.0
Release: 1%{?dist}
Summary: systemd nspawn container creation tool

License: GPLv3
URL: https://github.com/awood/salmon
Source0: https://github.com/awood/%{name}/archive/%{name}-%{version}-%{release}.tar.gz#/%{name}-%{version}-%{release}.tar.gz

BuildArch: noarch
BuildRequires: python2-devel
%if %{with python3}
BuildRequires: python3-devel
%endif # with python3

Requires: python-dnf
Requires: PyYaml

%description
Salmon is a tool for creating Systemd Nspawn containers.

%if %{with python3}
%package -n
Summary: systemd nspawn container creation tool

%description -n
Salmon is a tool for creating Systemd Nspawn containers.
%endif # with python3


%prep
%autosetup -c
mv %{name}-%{version} python2

%if %{with python3}
cp -a python2 python3
%endif # with python3


%build
pushd python2
%{__python2} setup.py build
popd

%if %{with python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with python3


%install
rm -rf $RPM_BUILD_ROOT
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with python3

pushd python2
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd


%check
pushd python2
%{__python2} setup.py test
popd

%if %{with python3}
pushd python3
%{__python3} setup.py test
popd
%endif


%files
%license python2/LICENSE
%doc python2/README.md
%{python2_sitelib}/*
%attr(755, root, root) %{_bindir}/salmon

%if %{with python3}
%files -n
%license python3/LICENSE
%doc python3/README
%{python3_sitelib}/*
%attr(755, root, root) %{_bindir}/salmon
%endif # with python3


%changelog
* Mon Sep 12 2016 Alex Wood <awood@redhat.com> 1.0.0-1
- Initial spec file.