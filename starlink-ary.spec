Summary:	ARY - subroutines for accessing ARRAY data structures
Summary(pl):	ARY - funkcje do dostêpu do tablicowych struktur danych (ARRAY)
Name:		starlink-ary
Version:	1.1_8.218
Release:	1
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.starlink.rl.ac.uk/pub/ussc/store/ary/ary.tar.Z
# Source0-md5:	77c27af971f0f14890ec02473f9d1c3f
URL:		http://www.starlink.rl.ac.uk/static_www/soft_further_ARY.html
BuildRequires:	gcc-g77
BuildRequires:	sed >= 4.0
BuildRequires:	starlink-err-devel
BuildRequires:	starlink-prm-devel
BuildRequires:	starlink-sae-devel
Requires:	starlink-sae
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		stardir		/usr/lib/star

%description
The ARY library is a set of routines for accessing Starlink ARRAY data
structures built using the Hierarchical Data System (HDS).

%description -l pl
Biblioteka ARY to zbiór funkcji s³u¿±cych do dostêpu do struktur danych
Starlink ARRAY (tablic) przy u¿yciu hierarchicznego systemu danych HDS.

%package devel
Summary:	Header files for ARY libraries
Summary(pl):	Pliki nag³ówkowe bibliotek ARY
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	starlink-err-devel
Requires:	starlink-prm-devel

%description devel
Header files for ARY libraries.

%description devel -l pl
Pliki nag³ówkowe bibliotek ARY.

%package static
Summary:	Static Starlink ARY libraries
Summary(pl):	Statyczne biblioteki Starlink ARY
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static Starlink ARY libraries.

%description static -l pl
Statyczne biblioteki Starlink ARY.

%prep
%setup -q -c

sed -i -e "s/ -O'/ %{rpmcflags} -fPIC'/" mk
sed -i -e "s/\\('-L\\\$(STAR_\\)LIB) /\\1SHARE) /;s/-lerr /&-lerr_standalone /;s/-lhds_adam/-lhds -lerr/;s/-lchr_adam -lprm_adam/-lchr -lprm/" makefile

%build
SYSTEM=ix86_Linux \
BLD_SHR='f() { g77 -shared $$3 -Wl,-soname=$$1 -o $$1 $$2;}; f' \
./mk build \
	STARLINK=%{stardir} \

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{stardir}/help

SYSTEM=ix86_Linux \
./mk install \
	STARLINK=%{stardir} \
	INSTALL=$RPM_BUILD_ROOT%{stardir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ary.news
%{stardir}/dates/*
%docdir %{stardir}/docs
%{stardir}/docs/sun*
%{stardir}/help/fac*
%attr(755,root,root) %{stardir}/share/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{stardir}/bin/ary_dev
%attr(755,root,root) %{stardir}/bin/ary_link*
%{stardir}/include/*

%files static
%defattr(644,root,root,755)
%{stardir}/lib/*.a
