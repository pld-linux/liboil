#
# Conditional build:
%bcond_without	tests	# don't perform "make check"
#
Summary:	Library of Optimized Inner Loops
Summary(pl):	Biblioteka zoptymalizowanych wewnêtrznych pêtli
Name:		liboil
Version:	0.3.0
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.schleef.org/liboil/download/%{name}-%{version}.tar.gz
# Source0-md5:	db1dc6b0dc1263a99075d5e34725636d
URL:		http://www.schleef.org/liboil/
BuildRequires:	glib2-devel >= 2.0
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
Liboil to biblioteka prostych funkcji zoptymalizowanych dla ró¿nych
procesorów. Funkcje te to zwykle pêtle implementuj±ce proste
algorytmy, takie jak konwersja tablicy N liczb ca³kowitych na liczby
zmiennoprzecinkowe albo mno¿enie i dodawanie tablicy N liczb. Takie
funkcje s± kandydatami do znacz±cej optymalizacji przy u¿yciu ró¿nych
technik, szczególnie poprzez u¿ycie rozszerzonych instrukcji
udostêpnianych przez nowoczesne procesory (Altivec, MMX, SSE itp.).

Wiele aplikacji multimedialnych i bibliotek ju¿ robi takie rzeczy
wewnêtrznie. Celem tego projektu jest po³±czenie czê¶ci kodu u¿ywanego
przez ró¿ne projekty multimedialne i u³atwienie u¿ywania optymalizacji
w szerszym zakresie aplikacji.

%package devel
Summary:	Header files for liboil library
Summary(pl):	Pliki nag³ówkowe biblioteki liboil
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for liboil library.

%description devel -l pl
Pliki nag³ówkowe biblioteki liboil.

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

%build
%configure
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
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/liboil-*.a
