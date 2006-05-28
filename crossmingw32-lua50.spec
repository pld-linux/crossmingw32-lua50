%define		realname	lua50
Summary:	A simple lightweight powerful embeddable programming language - Mingw32 cross version
Summary(pl):	Prosty, lekki ale pot�ny, osadzalny j�zyk programowania - wersja skro�na dla Mingw32
Name:		crossmingw32-%{realname}
Version:	5.0.2
Release:	5
License:	MIT
Group:		Development/Languages
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.gz
# Source0-md5:	dea74646b7e5c621fef7174df83c34b1
URL:		http://www.lua.org/
Requires:	crossmingw32-runtime
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-w32api
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

%description
Lua is a powerful, light-weight programming language designed for
extending applications. It is also frequently used as a
general-purpose, stand-alone language. It combines simple procedural
syntax (similar to Pascal) with powerful data description constructs
based on associative arrays and extensible semantics. Lua is
dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

%description -l pl
Lua to j�zyk programowania o du�ych mo�liwo�ciach ale lekki,
przeznaczony do rozszerzania aplikacji. Jest te� cz�sto u�ywany jako
samodzielny j�zyk og�lnego przeznaczenia. ��czy prost� proceduraln�
sk�adni� (podobn� do Pascala) z pot�nymi konstrukcjami opisu danych
bazuj�cymi na tablicach asocjacyjnych i rozszerzalnej sk�adni. Lua ma
dynamiczny system typ�w, interpretowany z bytecodu i automatyczne
zarz�dzanie pami�ci� z od�miecaczem, co czyni go idealnym do
konfiguracji, skrypt�w i szybkich prototyp�w.

%description -l pt_BR
Lua � uma linguagem de programa��o poderosa e leve, projetada para
estender aplica��es. Lua tamb�m � freq�entemente usada como uma
linguagem de prop�sito geral. Lua combina programa��o procedural com
poderosas constru��es para descri��o de dados, baseadas em tabelas
associativas e sem�ntica extens�vel. Lua � tipada dinamicamente,
interpretada a partir de bytecodes, e tem gerenciamento autom�tico de
mem�ria com coleta de lixo. Essas caracter�sticas fazem de Lua uma
linguagem ideal para configura��o, automa��o (scripting) e
prototipagem r�pida.

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
%{realname} - DLL library for Windows.

%description dll -l pl
%{realname} - biblioteka DLL dla Windows.

%prep
%setup -q -n lua-%{version}

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB
LDSHARED="%{target}-gcc -shared" ; export LDSHARED
TARGET="%{target}" ; export TARGET

%{__make} \
	MYCFLAGS="%{rpmcflags}" \
	CC="%{target}-gcc" \
	AR="%{target}-ar rcu" \
	RANLIB="%{target}-ranlib"

cd src
%{__cc} --shared *.o -Wl,--enable-auto-image-base -o ../lib/lua50.dll -Wl,--out-implib,../lib/liblua50.dll.a
cd lib
%{__cc} --shared *.o -Wl,--enable-auto-image-base -o ../../lib/lualib50.dll -Wl,--out-implib,../../lib/liblualib50.dll.a -llua -L../../lib
cd ../..

cd lib
mv liblua{,50}.a
mv liblualib{,50}.a
%if 0%{!?debug:1}
%{target}-strip *.dll
%{target}-strip -g -R.comment -R.note *.a
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{include/lua50,lib}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

install include/*.h $RPM_BUILD_ROOT%{arch}/include/lua50
install lib/*.a $RPM_BUILD_ROOT%{arch}/lib
install lib/*.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/*
%{arch}/lib/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system/*
