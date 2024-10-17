%define hg_date 20101106

Name: python-xpcom
Version: 2.0.0.0
Release: %mkrel 0.hg%{hg_date}.1
Summary: Python interface for mozilla XPCOM library
License: MPLv1.1 or GPLv2+ or LGPLv2+
Group: Development/Python
Url: https://developer.mozilla.org/en/PyXPCOM

Source: python-xpcom-%{version}.tar.bz2

Patch: xpcom-dynstr.patch

Requires: python  
Requires: xulrunner = %xulrunner_version
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
Requires: xulrunner-devel = %xulrunner_version

%description devel
Files needed to run Gecko applications written in python.

%prep
%setup -q -n pyxpcom-892b5462295b
%patch -p1

%build
autoconf-2.13
mkdir objdir
export CONFIGURE_TOP=`pwd`
pushd objdir
%configure2_5x --with-libxul-sdk=`pkg-config --variable=sdkdir libxul` --with-system-nspr
%make
popd

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
