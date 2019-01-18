echo #include ^<stdint.h^> > src\stdint.hpp
mkdir build
cd build
cmake -G"NMake Makefiles"                ^
-DCMAKE_INSTALL_PREFIX=%LIBRARY_PREFIX%  ^
      -DWITH_LIBSODIUM=ON                ^
      -DENABLE_DRAFTS=OFF                ^
      -DWITH_PERF_TOOL=OFF               ^
      -DZMQ_BUILD_TESTS=ON               ^
      -DENABLE_CPACK=OFF                 ^
      -DCMAKE_BUILD_TYPE=Release         ^
      -DCMAKE_EXE_LINKER_FLAGS='/STACK:8388608' ^
      ..
if errorlevel 1 exit 1

nmake install
if errorlevel 1 exit 1

copy /y %LIBRARY_BIN%\libzmq-mt-4*.dll /b %LIBRARY_BIN%\libzmq.dll
if errorlevel 1 exit 1

copy /y %LIBRARY_LIB%\libzmq-mt-4*.lib /b %LIBRARY_BIN%\libzmq.lib
if errorlevel 1 exit 1

nmake test
if errorlevel 1 exit 1

REM .\bin\test_ancillaries
REM if errorlevel 1 exit 1
REM .\bin\test_atomics
REM if errorlevel 1 exit 1
REM .\bin\test_base85
REM if errorlevel 1 exit 1
REM .\bin\test_bind_after_connect_tcp
REM if errorlevel 1 exit 1
REM .\bin\test_bind_src_address
REM if errorlevel 1 exit 1
REM .\bin\test_capabilities
REM if errorlevel 1 exit 1
REM .\bin\test_conflate
REM if errorlevel 1 exit 1
REM .\bin\test_connect_resolve
REM if errorlevel 1 exit 1
REM .\bin\test_connect_rid
REM if errorlevel 1 exit 1
REM .\bin\test_ctx_destroy
REM if errorlevel 1 exit 1
REM .\bin\test_ctx_options
REM if errorlevel 1 exit 1
REM .\bin\test_diffserv
REM if errorlevel 1 exit 1
REM .\bin\test_disconnect_inproc
REM if errorlevel 1 exit 1
REM .\bin\test_filter_ipc
REM .\bin\test_fork
REM .\bin\test_getsockopt_memset
REM .\bin\test_heartbeats
REM if errorlevel 1 exit 1
REM These fail frequently in version 4.2.5 on 32-bit Windows
REM .\bin\test_hwm
REM if errorlevel 1 exit 1
REM .\bin\test_hwm_pubsub
REM if errorlevel 1 exit 1
REM .\bin\test_immediate
REM if errorlevel 1 exit 1
REM .\bin\test_inproc_connect
REM if errorlevel 1 exit 1
REM .\bin\test_invalid_rep
REM if errorlevel 1 exit 1
REM .\bin\test_iov
REM if errorlevel 1 exit 1
REM .\bin\test_ipc_wildcard
REM .\bin\test_issue_566
REM if errorlevel 1 exit 1
REM .\bin\test_last_endpoint
REM if errorlevel 1 exit 1
REM .\bin\test_many_sockets
REM if errorlevel 1 exit 1
REM .\bin\test_metadata
REM if errorlevel 1 exit 1
REM .\bin\test_monitor
REM .\bin\test_msg_ffn
REM if errorlevel 1 exit 1
REM .\bin\test_msg_flags
REM if errorlevel 1 exit 1
REM .\bin\test_pair_inproc
REM if errorlevel 1 exit 1
REM .\bin\test_pair_ipc
REM .\bin\test_pair_tcp
REM if errorlevel 1 exit 1
REM .\bin\test_probe_router
REM if errorlevel 1 exit 1
REM .\bin\test_proxy
REM .\bin\test_proxy_single_socket
REM .\bin\test_proxy_terminate
REM .\bin\test_pub_invert_matching
REM if errorlevel 1 exit 1
REM .\bin\test_req_correlate
REM if errorlevel 1 exit 1
REM .\bin\test_req_relaxed
REM if errorlevel 1 exit 1
REM .\bin\test_reqrep_device
REM if errorlevel 1 exit 1
REM .\bin\test_reqrep_inproc
REM if errorlevel 1 exit 1
REM .\bin\test_reqrep_ipc
REM .\bin\test_reqrep_tcp
REM if errorlevel 1 exit 1
REM .\bin\test_router_handover
REM if errorlevel 1 exit 1
REM .\bin\test_router_mandatory
REM if errorlevel 1 exit 1
REM .\bin\test_router_mandatory_hwm
REM .\bin\test_security_null
REM if errorlevel 1 exit 1
REM .\bin\test_security_plain
REM if errorlevel 1 exit 1
REM .\bin\test_setsockopt
REM if errorlevel 1 exit 1
REM .\bin\test_sockopt_hwm
REM if errorlevel 1 exit 1
REM .\bin\test_sodium
REM if errorlevel 1 exit 1
REM .\bin\test_spec_dealer
REM if errorlevel 1 exit 1
REM .\bin\test_spec_pushpull
REM if errorlevel 1 exit 1
REM .\bin\test_spec_rep
REM if errorlevel 1 exit 1
REM .\bin\test_spec_req
REM if errorlevel 1 exit 1
REM .\bin\test_spec_router
REM if errorlevel 1 exit 1
REM .\bin\test_srcfd
REM if errorlevel 1 exit 1
REM .\bin\test_stream
REM if errorlevel 1 exit 1
REM .\bin\test_stream_disconnect
REM if errorlevel 1 exit 1
REM .\bin\test_stream_empty
REM if errorlevel 1 exit 1
REM .\bin\test_stream_exceeds_buffer
REM .\bin\test_stream_timeout
REM if errorlevel 1 exit 1
REM .\bin\test_sub_forward
REM if errorlevel 1 exit 1
REM .\bin\test_term_endpoint
REM if errorlevel 1 exit 1
REM .\bin\test_timeo
REM if errorlevel 1 exit 1
REM .\bin\test_unbind_inproc
REM if errorlevel 1 exit 1
REM .\bin\test_unbind_wildcard
REM if errorlevel 1 exit 1
REM .\bin\test_use_fd_ipc
REM .\bin\test_use_fd_tcp
REM if errorlevel 1 exit 1
REM .\bin\test_xpub_manual
REM if errorlevel 1 exit 1
REM .\bin\test_xpub_nodrop
REM if errorlevel 1 exit 1
REM .\bin\test_xpub_welcome_msg
REM if errorlevel 1 exit 1
REM .\bin\test_zmq_poll_fd

REM .\bin\test_security_curve
REM .\bin\test_shutdown_stress
REM .\bin\test_system
REM .\bin\test_thread_safe
