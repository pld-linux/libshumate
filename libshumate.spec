#
# Conditional build:
%bcond_without	apidocs		# API docs
%bcond_with	libsoup2	# libsoup2 instead of libsoup3 (must match libgweather4)

Summary:	Map widget for GTK 4
Summary(pl.UTF-8):	Widżet mapy dla GTK 4
Name:		libshumate
Version:	1.1.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.gnome.org/sources/libshumate/1.1/%{name}-%{version}.tar.xz
# Source0-md5:	15939dd12d83891b4fa724b7c7f20289
URL:		https://wiki.gnome.org/Projects/libshumate
BuildRequires:	cairo-devel >= 1.4
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.68.0
BuildRequires:	gobject-introspection-devel >= 0.6.3
BuildRequires:	gtk4-devel >= 4
BuildRequires:	json-glib-devel >= 1.6
BuildRequires:	meson >= 0.53.0
BuildRequires:	ninja >= 1.5
%{?with_libsoup2:BuildRequires:	libsoup-devel >= 2.42}
%{!?with_libsoup2:BuildRequires:	libsoup3-devel >= 3.0}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sqlite3-devel >= 3.0
BuildRequires:	vala >= 0.11.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	cairo >= 1.4
Requires:	glib2 >= 1:2.68.0
Requires:	json-glib >= 1.6
%{?with_libsoup2:Requires:	libsoup >= 2.42}
%{!?with_libsoup2:Requires:	libsoup3 >= 3.0}
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
Requires:	glib2-devel >= 1:2.68.0
Requires:	gtk4-devel >= 4
%{?with_libsoup2:Requires:	libsoup-devel >= 2.42}
%{!?with_libsoup2:Requires:	libsoup3-devel >= 3.0}
Requires:	sqlite3-devel >= 3.0

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
Requires:	gtk-doc-common
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
%meson build \
	%{!?with_apidocs:-Dgtk_doc=false} \
	%{?with_libsoup2:-Dlibsoup3=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
# FIXME: where to package gi-docgen generated docs?
install -d $RPM_BUILD_ROOT%{_gtkdocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libshumate-1.0 $RPM_BUILD_ROOT%{_gtkdocdir}
%endif

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
%{_gtkdocdir}/libshumate-1.0
%endif

%files -n vala-libshumate
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/shumate-1.0.deps
%{_datadir}/vala/vapi/shumate-1.0.vapi
