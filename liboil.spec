#
# Conditional build:
%bcond_without	altivec	# without Altivec support (on ppc)
%bcond_without	tests	# don't perform "make check"
#
Summary:	Library of Optimized Inner Loops
Summary(pl):	Biblioteka zoptymalizowanych wewn�trznych p�tli
Name:		liboil
Version:	0.3.2
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.schleef.org/liboil/download/%{name}-%{version}.tar.gz
# Source0-md5:	f127d90ee8531d03184b76f18e3997be
Patch0:		%{name}-opt.patch
Patch1:		%{name}-no_altivec.patch
URL:		http://www.schleef.org/liboil/
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake >= 1.6
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fomit-frame-pointer

%description
Liboil is a library of simple functions that are optimized for various
CPUs. These functions are generally loops implementing simple
algorithms, such as converting an array of N integers to
floating-poing numbers or multiplying and summing an array of N
numbers. Clearly such functions are candidates for significant
optimization using various techniques, especially by using extended
instructions provided by modern CPUs (Altivec, MMX, SSE, etc.).

Many multimedia applications and libraries already do similar things
internally. The goal of this project is to consolidate some of the
code used by various multimedia projects, and also make optimizations
easier to use by a broad range of applications.

%description -l pl
Liboil to biblioteka prostych funkcji zoptymalizowanych dla r�nych
procesor�w. Funkcje te to zwykle p�tle implementuj�ce proste
algorytmy, takie jak konwersja tablicy N liczb ca�kowitych na liczby
zmiennoprzecinkowe albo mno�enie i dodawanie tablicy N liczb. Takie
funkcje s� kandydatami do znacz�cej optymalizacji przy u�yciu r�nych
technik, szczeg�lnie poprzez u�ycie rozszerzonych instrukcji
udost�pnianych przez nowoczesne procesory (Altivec, MMX, SSE itp.).

Wiele aplikacji multimedialnych i bibliotek ju� robi takie rzeczy
wewn�trznie. Celem tego projektu jest po��czenie cz�ci kodu u�ywanego
przez r�ne projekty multimedialne i u�atwienie u�ywania optymalizacji
w szerszym zakresie aplikacji.

%package devel
Summary:	Header files for liboil library
Summary(pl):	Pliki nag��wkowe biblioteki liboil
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for liboil library.

%description devel -l pl
Pliki nag��wkowe biblioteki liboil.

%package static
Summary:	Static liboil library
Summary(pl):	Statyczna biblioteka liboil
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static liboil library.

%description static -l pl
Statyczna biblioteka liboil.

%prep
%setup -q
%patch0 -p1
%{!?with_altivec:%patch1 -p1}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} clean -C examples
cp -rf examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

rm -f $RPM_BUILD_ROOT%{_libdir}/liboiltmp1*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/liboil-*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liboil-*.so
%{_libdir}/liboil-*.la
%{_includedir}/liboil-*
%{_pkgconfigdir}/liboil-*.pc
%{_gtkdocdir}/liboil
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/liboil-*.a
