%define hg_rev 14

Name: python-xpcom
Version: 1.9.2
Release: %mkrel 1.hg%{hg_rev}.1
Summary: Python interface for mozilla XPCOM library
License: MPLv1.1 or GPLv2+ or LGPLv2+
Group: Development/Python
Url: http://developer.mozilla.org/en/PyXPCOM

# wget 'http://hg.mozilla.org/pyxpcom/archive/%%{hg_rev}.tar.bz2' -O python-xpcom-1.9.2-%%{hg_rev}.tar.bz2
Source: python-xpcom-1.9.2-%{hg_rev}.tar.bz2

Patch: xpcom-dynstr.patch

Requires: python  
Requires: xulrunner

BuildRequires: pkgconfig  
BuildRequires: libpython-devel  
BuildRequires: xulrunner-devel  
BuildRequires: zip  
BuildRequires: autoconf2.1

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}

%description
Files needed to run Gecko applications written in python.

%package devel
Summary: Development files for %{name}
Group: Development/C
Requires: %{name} = %{version}-%{release}
Requires: xulrunner-devel

%description devel
Files needed to run Gecko applications written in python.

%prep
%setup -q -n pyxpcom-%{hg_rev}
%patch -p1
autoconf-2.13

%build
mkdir -p objdir
cd objdir
echo -e '#!/bin/sh\n../configure "$@"' > configure
chmod u+x configure
%configure --with-libxul-sdk=`pkg-config --variable=sdkdir libxul` --with-system-nspr
make
cd -

%install
rm -rf %{buildroot}
_dst=%{buildroot}/%{python_sitelib}; install -d ${_dst} && cp -r objdir/dist/bin/python/* ${_dst}/
_dst=%{buildroot}/%{_libdir}/xulrunner-`pkg-config --modversion libxul`; install -d ${_dst} && cp -r objdir/dist/bin/* ${_dst}/
_dst=%{buildroot}/`pkg-config --variable=includedir libxul`; install -d ${_dst} && cp -r objdir/dist/include/* ${_dst}/
_dst=%{buildroot}/`pkg-config --variable=idldir libxul`; install -d ${_dst} && cp -r objdir/dist/idl/* ${_dst}/
_dst=%{buildroot}/`pkg-config --variable=sdkdir libxul`/sdk/lib; install -d ${_dst} && cp -r objdir/dist/lib/* ${_dst}/

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_libdir}/xulrunner-[0-9]*/*

%files devel
%{_includedir}/*
%{_libdir}/xulrunner-devel*/sdk/lib/*
%{_datadir}/idl/*
