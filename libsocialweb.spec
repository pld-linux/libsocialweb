#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
%bcond_without	vala		# do not build Vala API
#
Summary:	A social network data aggregator
Summary(pl.UTF-8):	Agregator danych z sieci społecznościowych
Name:		libsocialweb
Version:	0.25.20
Release:	2
License:	LGPL v2
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libsocialweb/0.25/%{name}-%{version}.tar.xz
# Source0-md5:	10332cd8674c39402e0834064e2b5437
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	intltool >= 0.40.0
BuildRequires:	json-glib-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libsoup-gnome-devel >= 2.26.0
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	pkgconfig
BuildRequires:	rest-devel >= 0.7.10
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 1:0.12}
BuildRequires:	xz
Requires:	rest >= 0.7.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libsocialweb is a social data server which fetches data from the
"social web", such as your friend's blog posts and photos, upcoming
events, recently played tracks, and pending eBay auctions. It also
provides a service to update your status on web services which support
it, such as MySpace and Twitter.

%description -l pl.UTF-8
libsocialweb to serwer danych społecznościowych, pobierający dane z
"serwisów społecznościowych", takie jak posty i zdjęcia z blogów
znajomych, zbliżające się wydarzenia, ostatnio odtwarzane utwory,
zbliżające się aukcje na eBayu. Udostępnia także usługę uaktualniającą
stan użytkownika na serwisach WWW, które to obsługują - np. MySpace
czy Twitter.

%package devel
Summary:	Header files for socialweb library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki socialweb
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-glib-devel
Requires:	glib2-devel >= 1:2.16.0
Requires:	libsoup-devel >= 2.26.0
Requires:	rest-devel >= 0.7.10

%description devel
Header files for socialweb library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki socialweb.

%package static
Summary:	Static socialweb library
Summary(pl.UTF-8):	Statyczna biblioteka socialweb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static socialweb library.

%description static -l pl.UTF-8
Statyczna biblioteka socialweb.

%package apidocs
Summary:	socialweb library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki socialweb
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for socialweb library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki socialweb.

%package -n vala-libsocialweb
Summary:	libsocialweb API for Vala language
Summary(pl.UTF-8):	API libsocialweb dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description -n vala-libsocialweb
libsocialweb API for Vala language.

%description -n vala-libsocialweb -l pl.UTF-8
API libsocialweb dla języka Vala.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{__enable_disable apidocs gtk-doc} \
	%{__enable_disable static_libs static} \
	--enable-all-services \
	%{__enable_disable vala vala-bindings} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la \
	$RPM_BUILD_ROOT%{_libdir}/libsocialweb/services/*.la

%if %{with static_libs}
	%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsocialweb/services/*.a
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libexecdir}/libsocialweb-core
%attr(755,root,root) %{_libdir}/libsocialweb-client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsocialweb-client.so.2
%attr(755,root,root) %{_libdir}/libsocialweb-keyfob.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsocialweb-keyfob.so.0
%attr(755,root,root) %{_libdir}/libsocialweb-keystore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsocialweb-keystore.so.0
%attr(755,root,root) %{_libdir}/libsocialweb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsocialweb.so.0
%dir %{_libdir}/libsocialweb
%dir %{_libdir}/libsocialweb/services
%attr(755,root,root) %{_libdir}/libsocialweb/services/libfacebook.so
%attr(755,root,root) %{_libdir}/libsocialweb/services/libflickr.so
%attr(755,root,root) %{_libdir}/libsocialweb/services/liblastfm.so
%attr(755,root,root) %{_libdir}/libsocialweb/services/libmyspace.so
%attr(755,root,root) %{_libdir}/libsocialweb/services/libphotobucket.so
%attr(755,root,root) %{_libdir}/libsocialweb/services/libplurk.so
%attr(755,root,root) %{_libdir}/libsocialweb/services/libsina.so
%attr(755,root,root) %{_libdir}/libsocialweb/services/libsmugmug.so
%attr(755,root,root) %{_libdir}/libsocialweb/services/libtwitter.so
%attr(755,root,root) %{_libdir}/libsocialweb/services/libvimeo.so
%attr(755,root,root) %{_libdir}/libsocialweb/services/libyoutube.so
%{_libdir}/girepository-1.0/SocialWebClient-0.25.typelib
%{_datadir}/dbus-1/services/libsocialweb.service
%{_datadir}/libsocialweb

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsocialweb-client.so
%attr(755,root,root) %{_libdir}/libsocialweb-keyfob.so
%attr(755,root,root) %{_libdir}/libsocialweb-keystore.so
%attr(755,root,root) %{_libdir}/libsocialweb.so
%{_datadir}/gir-1.0/SocialWebClient-0.25.gir
%{_includedir}/libsocialweb
%{_pkgconfigdir}/libsocialweb-client.pc
%{_pkgconfigdir}/libsocialweb-keyfob.pc
%{_pkgconfigdir}/libsocialweb-keystore.pc
%{_pkgconfigdir}/libsocialweb-module.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsocialweb-client.a
%{_libdir}/libsocialweb-keyfob.a
%{_libdir}/libsocialweb-keystore.a
%{_libdir}/libsocialweb.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libsocialweb-client
%{_gtkdocdir}/libsocialweb-dbus
%{_gtkdocdir}/libsocialweb
%endif

%if %{with vala}
%files -n vala-libsocialweb
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libsocialweb-client.deps
%{_datadir}/vala/vapi/libsocialweb-client.vapi
%endif
