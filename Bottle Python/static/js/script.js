$(document).ready( function() {
    $.ajax({
            url : 'http://127.0.0.1:8080/ModemStats/api',
            type: 'GET',
            dataType: 'json',
                }).done(function(data) {
                        console.log(data);
                        var uptime =(data.ModemStats[0].result).replace("b'","");
                        uptime = uptime.split("\\n'");
                        $("#uptime").html(uptime);
                        $("#ip").html(data.ModemStats[1].result);
                         
                        var diskusage =data.ModemStats[2].result.replace("b'","");
                        diskusage = diskusage.replace("\n","<br>")
                         $("#DiskUsage").html(diskusage)


                         var routeTable =data.ModemStats[3].result.replace("b'","");
                        routeTable = routeTable.replace("\n","<br>");
                         $("#RouteTable").html(routeTable);

                         var imei = data.ModemStats[4].result.replace("b'","");
                         imei = imei.replace("\n","<br>");
                         $('#imei').html(imei);

                         var ss = data.ModemStats[5].result.replace("b'","");
                         ss = ss.replace("\n","<br>");
                         $('#signal').html(ss);

                         var lac = data.ModemStats[6].result.replace("b'","");
                         lac = lac.replace("\n","<br>");
                         $('#lacinfo').html(lac);

                         var data = data.ModemStats[7].result.replace("b'","");
                         data = data.replace("\n","<br>");
                         $('#DataUsage').html(data);
                            });
                            });
