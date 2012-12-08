Summary:	GNOME Settings Daemon
Name:		gnome-settings-daemon
Version:	3.6.3
Release:	3
Epoch:		1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-settings-daemon/3.6/%{name}-%{version}.tar.xz
# Source0-md5:	1736e7305439b027cc7c2de2899ded69
Patch0:		%{name}-bug680689.patch
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	colord-devel
BuildRequires:	cups-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-desktop-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	intltool
BuildRequires:	lcms2-devel
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libnotify-devel
BuildRequires:	libtool
BuildRequires:	libwacom-devel
BuildRequires:	libxklavier-devel
BuildRequires:	pkg-config
BuildRequires:	pulseaudio-devel
BuildRequires:	systemd-devel
BuildRequires:	udev-glib-devel
BuildRequires:	upower-devel
BuildRequires:	xorg-driver-input-wacom-devel
BuildRequires:	xorg-libXxf86misc-devel
BuildRequires:	xorg-libxkbfile-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}-3.0

%description
GNOME Settings Daemon.

%package devel
Summary:	Header file for developing GNOME Settings Daemon clients
Group:		Development/Libraries

%description devel
Header file for developing GNOME Settings Daemon clients.

%prep
%setup -q
%patch0 -p1

# packagekit not used (yet)
%{__sed} -i '/<child name="updates".*/d' \
	data/org.gnome.settings-daemon.plugins.gschema.xml.in.in

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-ibus		\
	--disable-packagekit	\
	--disable-silent-rules	\
	--disable-static	\
	--enable-systemd
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-3.0/gtk-modules

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-3.0/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw,ha,ig,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_icon_cache hicolor
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README plugins/common/input-device-example.sh
%dir %{_libexecdir}
%dir %{_libexecdir}/gtk-modules
%attr(755,root,root) %{_libexecdir}/*.so
%attr(755,root,root) %{_libexecdir}/gnome-*
%attr(755,root,root) %{_libexecdir}/gnome-settings-daemon
%attr(755,root,root) %{_libexecdir}/gsd-*
%{_libexecdir}/*-plugin

%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/gnome-settings-daemon
%{_datadir}/polkit-1/actions/org.gnome.settings-daemon.plugins.power.policy
%{_datadir}/polkit-1/actions/org.gnome.settings-daemon.plugins.wacom.policy
%{_sysconfdir}/xdg/autostart/gnome-fallback-mount-helper.desktop
%{_sysconfdir}/xdg/autostart/gnome-settings-daemon.desktop
%{_iconsdir}/hicolor/*/*/*.*
%{_mandir}/man1/gnome-settings-daemon.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/gnome-settings-daemon-3.0
%{_pkgconfigdir}/gnome-settings-daemon.pc

