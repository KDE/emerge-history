; This script will detect which Version of Windows is running.
; Modified from the NSIS Wiki, thanks to dragonbals@hotmail.com

Function getWindowsVersion
; Returns the windows version: 95, 98, ME, 2000, 2003, Vista or 7 in $0
    Push $R1
    ClearErrors

    ReadRegStr $R0 HKLM \
       "SOFTWARE\Microsoft\Windows NT\CurrentVersion" CurrentVersion

    IfErrors 0 lbl_winnt

    ; we are not NT
    ReadRegStr $R0 HKLM \
       "SOFTWARE\Microsoft\Windows\CurrentVersion" VersionNumber

    StrCpy $R1 $R0 1
    StrCmp $R1 '4' 0 lbl_error

    StrCpy $R1 $R0 3

    StrCmp $R1 '4.0' lbl_win32_95
    StrCmp $R1 '4.9' lbl_win32_ME lbl_win32_98

    lbl_win32_95:
        StrCpy $R0 '95'
    Goto lbl_done

    lbl_win32_98:
        StrCpy $R0 '98'
    Goto lbl_done

    lbl_win32_ME:
        StrCpy $R0 'ME'
    Goto lbl_done

    lbl_winnt:

    StrCpy $R1 $R0 1

    StrCmp $R1 '3' lbl_winnt_x
    StrCmp $R1 '4' lbl_winnt_x

    StrCpy $R1 $R0 3

    StrCmp $R1 '5.0' lbl_winnt_2000
    StrCmp $R1 '5.1' lbl_winnt_XP
    StrCmp $R1 '5.2' lbl_winnt_2003
    StrCmp $R1 '6.0' lbl_winnt_vista
    StrCmp $R1 '6.1' lbl_winnt_7 lbl_error

    lbl_winnt_x:
        StrCpy $R0 "NT $R0" 6

    Goto lbl_done

    lbl_winnt_2000:
        Strcpy $R0 '2000'
    Goto lbl_done

    lbl_winnt_XP:
        Strcpy $R0 'XP'
    Goto lbl_done

    lbl_winnt_2003:
        Strcpy $R0 '2003'
    Goto lbl_done

    lbl_winnt_vista:
        Strcpy $R0 'Vista'
    Goto lbl_done

    lbl_winnt_7:
        Strcpy $R0 '7'
    Goto lbl_done

    lbl_error:
        Strcpy $R0 ''
    lbl_done:

  Pop $R1
FunctionEnd
