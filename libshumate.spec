#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	sysprof		# sysprof profiling

Summary:	Map widget for GTK 4
Summary(pl.UTF-8):	Widżet mapy dla GTK 4
Name:		libshumate
Version:	1.4.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.gnome.org/sources/libshumate/1.4/%{name}-%{version}.tar.xz
# Source0-md5:	0140aaa4891ac215d0f40b4ad4cd880d
URL:		https://gnome.pages.gitlab.gnome.org/libshumate/
BuildRequires:	cairo-devel >= 1.4
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.74.0
BuildRequires:	gobject-introspection-devel >= 0.6.3
BuildRequires:	gtk4-devel >= 4
BuildRequires:	json-glib-devel >= 1.6
BuildRequires:	meson >= 0.55.0
BuildRequires:	ninja >= 1.5
BuildRequires:	libsoup3-devel >= 3.0
BuildRequires:	protobuf-c-devel
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sqlite3-devel >= 3.0
%{?with_sysprof:BuildRequires:	sysprof-devel >= 3.38}
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 0.11.0
BuildRequires:	xz
Requires:	cairo >= 1.4
Requires:	glib2 >= 1:2.74.0
Requires:	json-glib >= 1.6
Requires:	libsoup3 >= 3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libshumate is a GTK 4 widget to display maps.

%description -l pl.UTF-8
Libshumate to widżet GTK 4 do wyświetlania map.

%package devel
Summary:	Header files for the libshumate library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libshumate
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cairo-devel >= 1.4
Requires:	glib2-devel >= 1:2.74.0
Requires:	gtk4-devel >= 4
Requires:	json-glib-devel >= 1.6
Requires:	libsoup3-devel >= 3.0
Requires:	protobuf-c-devel
Requires:	sqlite3-devel >= 3.0
%if %{with sysprof}
Requires:	sysprof-devel >= 3.38
%endif

%description devel
Header files for the libshumate library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libshumate.

%package static
Summary:	Static libshumate libraries
Summary(pl.UTF-8):	Statyczne biblioteki libshumate
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libshumate libraries.

%description static -l pl.UTF-8
Statyczne biblioteki libshumate.

%package apidocs
Summary:	libshumate API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libshumate
Group:		Documentation
BuildArch:	noarch

%description apidocs
libshumate API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libshumate.

%package -n vala-libshumate
Summary:	libshumate API for Vala language
Summary(pl.UTF-8):	API libshumate dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 0.15.1
BuildArch:	noarch

%description -n vala-libshumate
libshumate API for Vala language.

%description -n vala-libshumate -l pl.UTF-8
API libshumate dla języka Vala.

%prep
%setup -q

%build
%meson \
	%{!?with_apidocs:-Dgtk_doc=false} \
	-Dsysprof=%{__enabled_disabled sysprof}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libshumate-1.0 $RPM_BUILD_ROOT%{_gidocdir}
%endif

# not supported by glibc (as of 2.38)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang shumate1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f shumate1.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libshumate-1.0.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libshumate-1.0.so.1
%{_libdir}/girepository-1.0/Shumate-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libshumate-1.0.so
%{_includedir}/shumate-1.0
%{_pkgconfigdir}/shumate-1.0.pc
%{_datadir}/gir-1.0/Shumate-1.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libshumate-1.0.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libshumate-1.0
%endif

%files -n vala-libshumate
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/shumate-1.0.deps
%{_datadir}/vala/vapi/shumate-1.0.vapi
