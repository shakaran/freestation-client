#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet 

class DataProvider:
    
    def __init__(self):
        
        self.data = {
                     'panel': 
                         {
                               'distribution': """<div style="overflow:auto;height:750px;
                                                    border-radius:10px;background-color:#AA0000;border:3px solid black;margin-right:50px;padding:10px">
                                                        <div class="second_option" id="molinux_button"  onclick="javascript:get_description('molinux')" class="zone_hover" style="margin-bottom:70px">
                                                            <div class="legend_box">
                                                               <img class="bhover" style="position:relative;top:-50px;height:100px" 
                                                               src="img/client/molinux-button.png" title="MoLinux">
                                                               <div style="position:relative;top:-40px">
                                                                    Fecha: 10-07-2012 Version: 7.0
                                                               </div>
                                                               <div id="molinux_status" style="float:right"></div>
                                                            </div>
                                                        </div>
                                                        <div class="second_option" id="debian_button"  onclick="javascript:get_description('debian')" class="zone_hover" style="margin-bottom:70px">
                                                            <div class="legend_box">
                                                               <img class="bhover" style="position:relative;top:-50px;height:100px" 
                                                               src="img/client/debian-button.png" title="Debian">
                                                               <div style="position:relative;top:-40px">
                                                                    Fecha: 18-07-2012 Version: 6.0
                                                               </div>
                                                               <div id="debian_status" style="float:right"></div>
                                                            </div>
                                                        </div>
                                                        <div class="second_option" id="ubuntu_button" onclick="javascript:get_description('ubuntu')" class="zone_hover" style="margin-bottom:70px">
                                                            <div class="legend_box">
                                                               <img class="bhover" style="position:relative;top:-50px;height:100px" 
                                                               src="img/client/ubuntu-button.png" title="Ubuntu">
                                                               <div style="position:relative;top:-40px">
                                                                    Fecha: 29-04-2012 Version: 12.04
                                                               </div>
                                                               <div id="ubuntu_status" style="float:right"></div>
                                                            </div>
                                                        </div>
                                                        <div class="second_option" id="arch_button"  onclick="javascript:get_description('arch')" class="zone_hover" style="margin-bottom:70px">
                                                            <div class="legend_box">
                                                               <img class="bhover" style="position:relative;top:-50px;height:100px" 
                                                               src="img/client/arch-button.png" title="Arch">
                                                               <div style="position:relative;top:-40px">
                                                                    Fecha: 03-02-2011 Version: 2.0
                                                               </div>
                                                               <div id="arch_status" style="float:right"></div>
                                                            </div>
                                                        </div>
                                                        <div class="second_option" id="gentoo_button" onclick="javascript:get_description('gentoo')"  class="zone_hover" style="margin-bottom:70px">
                                                            <div class="legend_box">
                                                               <img class="bhover" style="position:relative;top:-50px;height:100px" 
                                                               src="img/client/gentoo-button.png" title="Gentoo">
                                                               <div style="position:relative;top:-40px">
                                                                    Fecha: 20-10-2012 Version: 4.0
                                                               </div>
                                                               <div id="gentoo_status" style="float:right"></div>
                                                            </div>
                                                        </div>
                                                        <div class="second_option" id="centos_button" onclick="javascript:get_description('centos')" class="zone_hover" style="margin-bottom:70px">
                                                            <div class="legend_box">
                                                               <img class="bhover" style="position:relative;top:-50px;height:100px" 
                                                               src="img/client/centos-button.png" title="CentOs">
                                                               <div style="position:relative;top:-40px">
                                                                    Fecha: 04-04-2012 Version: 6.3
                                                               </div>
                                                               <div id="centos_status" style="float:right"></div>
                                                            </div>
                                                        </div>
                                                    </div>""",
                            'software' : 
                            """
                            <div style="overflow:auto;height:750px;border-radius:10px;background-color:#AA0000;border:3px solid black;margin-right:50px;padding:10px">
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('software', 'gimp')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/gimp.png" title="Gimp">
                                       
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">GIMP</span>
                                           <br />
                                           <br />
                                           Potente editor de imágenes multiplataforma
                                           <br />
                                           Fecha: 13-08-2012 Version: 2.8
                                       </div>
                                    </div>
                                </div>
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('software', 'gimp')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/blender.png" title="Blender">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">Blender</span>
                                           <br />
                                           <br />
                                           Programa multiplataforma, para modelado, animación y creación de gráficos tridimensionales
                                           <br />
                                           Fecha: 13-08-2012 Version: 2.63
                                       </div>
                                    </div>
                                </div>
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('software', 'gimp')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/inkscape.png" title="Gimp">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">InkScape</span>
                                           <br />
                                           <br />
                                           Editor de gráficos en formato vectoriales SVG, gratuito, libre y multiplataforma
                                           <br />
                                           Fecha: 13-08-2012 Version: 2.8
                                       </div>
                                    </div>
                                </div>
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('software', 'gimp')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/vlc.png" title="Gimp">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">VLC</span>
                                           <br />
                                           <br />
                                           Reproductor multimedia y framework multimedia libre y de código abierto
                                           <br />
                                           Fecha: 13-08-2012 Version: 2.0.2
                                       </div>
                                    </div>
                                </div>
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('software', 'gimp')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/libreoffice.png" title="Gimp">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">LibreOffice</span>
                                           <br />
                                           <br />
                                           Suite ofimática libre y gratuita, compatible con Microsoft Windows, Mac y GNU/Linux
                                           <br />
                                           Fecha: 13-08-2012 Version: 3.6
                                       </div>
                                    </div>
                                </div>
                            </div>
                            """,
                            'resources' : 
                            """
                            <div style="overflow:auto;height:750px;border-radius:10px;background-color:#AA0000;border:3px solid black;margin-right:50px;padding:10px">
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('resources', 'resource1')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/resource.png" title="Gimp">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">Recurso 1</span>
                                           <br />
                                           <br />
                                           Descripcion Recurso 1
                                           <br />
                                           Fecha: 13-08-2012 Version: 3.6
                                       </div>
                                    </div>
                                </div>
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('resources', 'resource2')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/resource.png" title="Gimp">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">Recurso 2</span>
                                           <br />
                                           <br />
                                           Descripcion Recurso 2
                                           <br />
                                           Fecha: 13-08-2012 Version: 3.6
                                       </div>
                                    </div>
                                </div>
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('resources', 'resource3')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/resource.png" title="Gimp">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">Recurso 3</span>
                                           <br />
                                           <br />
                                           Descripcion Recurso 3
                                           <br />
                                           Fecha: 13-08-2012 Version: 3.6
                                       </div>
                                    </div>
                                </div>
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('resources', 'resource4')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/resource.png" title="Gimp">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">Recurso 4</span>
                                           <br />
                                           <br />
                                           Descripcion Recurso 4
                                           <br />
                                           Fecha: 13-08-2012 Version: 3.6
                                       </div>
                                    </div>
                                </div>
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('resources', 'resource5')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/resource.png" title="Gimp">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">Recurso 5</span>
                                           <br />
                                           <br />
                                           Descripcion Recurso 5
                                           <br />
                                           Fecha: 13-08-2012 Version: 3.6
                                       </div>
                                    </div>
                                </div>
                            </div>
                            """,
                            'documentation' : 
                            """
                            <div style="overflow:auto;height:750px;border-radius:10px;background-color:#AA0000;border:3px solid black;margin-right:50px;padding:10px">
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('documentation', 'manual1')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/manual.png" title="Manual">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">Manual 1</span>
                                           <br />
                                           <br />
                                           Descripción manual 1
                                           <br />
                                           Fecha: 13-08-2012 Version: 3.6
                                       </div>
                                    </div>
                                </div>
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('documentation', 'manual2')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/manual.png" title="Manual">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">Manual 2</span>
                                           <br />
                                           <br />
                                           Descripción manual 2
                                           <br />
                                           Fecha: 13-08-2012 Version: 3.6
                                       </div>
                                    </div>
                                </div>
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('documentation', 'manual3')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/manual.png" title="Manual">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">Manual 3</span>
                                           <br />
                                           <br />
                                           Descripción manual 3
                                           <br />
                                           Fecha: 13-08-2012 Version: 3.6
                                       </div>
                                    </div>
                                </div>
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('documentation', 'manual4')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/manual.png" title="Manual">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">Manual 4</span>
                                           <br />
                                           <br />
                                           Descripción manual 4
                                           <br />
                                           Fecha: 13-08-2012 Version: 3.6
                                       </div>
                                    </div>
                                </div>
                                <div class="second_option" id="gimp_button"  onclick="javascript:get_description('documentation', 'manual5')" class="zone_hover" style="margin-bottom:70px">
                                    <div class="legend_box">
                                       <img class="bhover" style="position:relative;top:-50px;height:100px" src="img/manual.png" title="Manual">
                                       <div style="position:relative;top:-60px">
                                           <span style="font-size:22px;text-align:center">Manual 5</span>
                                           <br />
                                           <br />
                                           Descripción manual 5
                                           <br />
                                           Fecha: 13-08-2012 Version: 3.6
                                       </div>
                                    </div>
                                </div>
                            </div>
                            """,
                            'home_news' : 
                            """
                            <div id="welcome_panel">
                                <h1>¡Bienvenido a FreeStation!</h1>
                            
                                <div style="color:#b7b3b3;">
                                    
                                    <h2>Punto de información</h2>
                                
                                    <div style="height:400px;width:300px;float:left;padding:10px;text-align:left;border: 3px dotted #613854;background:#853d6e">
                                        <h3 style="text-decoration:underline">Novedades</h3>
                                        <ul>
                                            <li>Novedad: Incorporada nueva versión de la distribución Debian 7.0</li>
                                            <li>Novedad: Versión 1.5 liberada</li>
                                            <li>Novedad: FreeStation dispone de más de 2000 POIs instalados</li>
                                            <li>Corrección: arreglado fallo en la disposición de paneles</li>
                                        </ul>
                                    </div>
                                    
                                    <div style="float:right;width:200px;padding:10px;text-align:left;border: 3px dotted #613854;background:#853d6e">
                                        <h3 style="text-decoration:underline">Categorías</h3>
                                        <ul>
                                            <li>Aplicaciones</li>
                                            <li>Exámenes</li>
                                            <li>Docencia</li>
                                            <li>Investigación</li>
                                        </ul>
                                    </div>
                    
                                </div>
                            </div>
                            """,
                            'home' : 
                            """
                            <script>
                                console.log('load home from script')
                            </script>
                            <div class="first_option" id="distributions_button"  onclick="javascript:on_press_distributions()" class="zone_hover" style="margin-bottom:60px">
                                <div class="legend_box" style="height:120px">
                                   <img class="bhover" style="position:relative;top:-50px;height:60px" src="img/client/distributions-button.png" title="Inicio">
                                   <div style="position:relative;top:-40px">
                                        Descargar ISO de distribuciones GNU/Linux
                                        <br />
                                        Software libre empaquetado con los mejores
                                        programas seleccionados
                                   </div>
                                </div>
                            </div>
                            <div class="first_option" id="software_button" onclick="javascript:on_press_software()" class="zone_hover" style="margin-bottom:60px">
                                <div class="legend_box" style="height:120px">
                                   <img class="bhover" style="position:relative;top:-50px;height:60px" src="img/client/software-button.png" title="Inicio">
                                   <div style="position:relative;top:-40px">
                                        Descarga software libre para Windows con
                                        características excelentes
                                   </div>
                                </div>
                            </div>
                            <div class="first_option" id="documentation_button" onclick="javascript:on_press_documentation()" class="zone_hover" style="margin-bottom:60px">
                                <div class="legend_box" style="height:120px">
                                   <img class="bhover" style="position:relative;top:-50px;height:60px" src="img/client/documentation-button.png" title="Inicio">
                                   <div style="position:relative;top:-40px">
                                        Manuales de software
                                        <br />
                                        Los principales manuales elaborados por temática.
                                   </div>
                                </div>
                            </div>
                            <div class="first_option" id="resources_button" onclick="javascript:on_press_resources()" class="zone_hover" style="margin-bottom:60px">
                                <div class="legend_box" style="height:120px">
                                   <img class="bhover" style="position:relative;top:-50px;height:60px" src="img/client/resources-button.png" title="Inicio">
                                   <div style="position:relative;top:-40px">
                                        Apuntes de asignaturas
                                        <br />
                                        Documentos de interés para alumnado y transparencias de
                                        asignaturas.
                                   </div>
                                </div>
                            </div>
                            """,
                            'right_description' : 
                            """
                            <div>
                                <h1>Descripción</h1>
                                <div id="description_content" style="border:3px solid black;padding:10px;height:300px;3px solid black;border-radius:10px;background:#D35F5F;color:white;overflow:auto">
                                   Una distribución de Gnu/Linux es una distribución de software 
                            basada en el núcleo Linux que incluye determinados paquetes de 
                            software para satisfacer las necesidades de un grupo específico 
                            de usuarios, dando así origen a ediciones domésticas, 
                            empresariales y para servidores. 
                            <br /><br />
                            En general, las distribuciones Linux pueden ser:<br />
                                * Comerciales o no comerciales.<br />
                                * Ser completamente libres o incluir software privativo.<br />
                                * Diseñadas para uso en el hogar o en las empresas.<br />
                                * Diseñadas para servidores, escritorios o dispositivos empotrados.<br />
                                * Orientadas a usuarios regulares o usuarios avanzados.<br />
                            <br /><br />
                            Es un sistema operativo muy completo, con un escritorio sencillo y cómodo. 
                            Lleva "de serie" el software necesario para las tareas más habituales: <br />
                                * Conectarse a Internet<br />
                                * Mensajería instantánea<br />
                                * Navegación web<br />
                                * Gestor de correo electrónico<br />
                            <br />
                            Además, también dispone de todas las funciones de edición de 
                            textos, hojas de cálculo, 
                            bases de datos, edición de imágenes, etc.
                            <br /><br />
                            En la actualidad existen gran cantidad de distribuciones, 
                            cada una de ellas creada para satisfacer unas necesidades 
                            concretas y con un objetivo específico, como es la facilidad 
                            de uso, la seguridad, su utilización por un colectivo determinado, 
                            etc, 
                            <br /><br />
                            Las distribuciones GNU/Linux vienen completamente pre-configuradas 
                            según las especificaciones establecidas por la organización que 
                            las crea, incluyendo utilidades e instaladores.
                            <br /><br />
                            La mayoría de las distribuciones están, en mayor o menor medida, 
                            desarrolladas y dirigidas por sus comunidades de desarrolladores y 
                            usuarios. En algunos casos están dirigidas y financiadas 
                            completamente por la comunidad. como ocurre con Debian GNU/Linux, 
                            mientras que otras mantienen una distribución comercial y una 
                            versión de la comunidad.
                                </div>
                                <div id="usb_info">
                                    Detector de USB: No presente<br />
                                </div>
                                <br />
                                <progress style="display:none" id="bar" value="50" max="100"></progress>
                                <div style="width:100%;height:450px">
                                    <div style="color:white;font-size:25px">Copiar a USB</div>
                                    
                                    <div>
                                        <img id="copyusb" onclick="javacript:on_press_copy_usb()" style="height:75px" src="img/client/copy-usb-button.png" title="Copiar a USB" />
                                        <span id="copyusb_message"></span>
                                    </div>
                                    
                                    <div style="color:white;font-size:25px">Crear USB Bootable</div>
                                    
                                    <div>
                                        <img style="height:75px" src="img/client/usb-bootable-button.png" title="Crear USB Bootable" />
                                    </div>
                                </div>
                            </div>
                            """,
                            
                      },
                     'description' : 
                        {
                         'distribution' : 
                         {
                             'default': """ Una distribución de Gnu/Linux es una distribución de software 
                                            basada en el núcleo Linux que incluye determinados paquetes de 
                                            software para satisfacer las necesidades de un grupo específico 
                                            de usuarios, dando así origen a ediciones domésticas, 
                                            empresariales y para servidores. 
                                            <br /><br />
                                            En general, las distribuciones Linux pueden ser:<br />
                                                * Comerciales o no comerciales.<br />
                                                * Ser completamente libres o incluir software privativo.<br />
                                                * Diseñadas para uso en el hogar o en las empresas.<br />
                                                * Diseñadas para servidores, escritorios o dispositivos empotrados.<br />
                                                * Orientadas a usuarios regulares o usuarios avanzados.<br />
                                            <br /><br />
                                            Es un sistema operativo muy completo, con un escritorio sencillo y cómodo. 
                                            Lleva "de serie" el software necesario para las tareas más habituales: <br />
                                                * Conectarse a Internet<br />
                                                * Mensajería instantánea<br />
                                                * Navegación web<br />
                                                * Gestor de correo electrónico<br />
                                            <br />
                                            Además, también dispone de todas las funciones de edición de 
                                            textos, hojas de cálculo, 
                                            bases de datos, edición de imágenes, etc.
                                            <br /><br />
                                            En la actualidad existen gran cantidad de distribuciones, 
                                            cada una de ellas creada para satisfacer unas necesidades 
                                            concretas y con un objetivo específico, como es la facilidad 
                                            de uso, la seguridad, su utilización por un colectivo determinado, 
                                            etc, 
                                            <br /><br />
                                            Las distribuciones GNU/Linux vienen completamente pre-configuradas 
                                            según las especificaciones establecidas por la organización que 
                                            las crea, incluyendo utilidades e instaladores.
                                            <br /><br />
                                            La mayoría de las distribuciones están, en mayor o menor medida, 
                                            desarrolladas y dirigidas por sus comunidades de desarrolladores y 
                                            usuarios. En algunos casos están dirigidas y financiadas 
                                            completamente por la comunidad. como ocurre con Debian GNU/Linux, 
                                            mientras que otras mantienen una distribución comercial y una 
                                            versión de la comunidad.""",
                                'molinux': """  <h3>MOLINUX</h3>
                                                <br /><br />
                                                <b>MoLinux</b> es la distribución GNU/Linux oficial de la Junta de 
                                                Comunidades de Castilla-La Mancha. MoLinux está basado en Ubuntu.<br /> 
                                                <br />
                                                Los nombres de cada versión son personajes de la novela 
                                                "<i>El ingenioso hidalgo don Quijote de la Mancha</i>", de Miguel de 
                                                Cervantes.<br />
                                                <br />
                                                MoLinux es una iniciativa comenzada en 2005 de la JCCM para 
                                                introducir a la comunidad castellano-manchega en la vanguardia 
                                                de la Sociedad de la Información. El proyecto MoLinux ataca la 
                                                brecha digital reduciendo los costes del software y ofreciendo 
                                                un sistema operativo fácil de usar. MoLinux es un sistema operativo 
                                                general. Pronto estarán disponibles versiones modulares adaptadas 
                                                a usos más específicos.<br />
                                                <br />
                                                El compromiso con la filosofía 'software libre' es tal que el 
                                                gobierno castellano manchego no impondrá en ningún caso el uso 
                                                de 'Molinux'. "La ventaja es que el 'software' libre no tiene que 
                                                competir con nadie, y el usuario puede elegir entre usar este u otro 
                                                tipo de 'software'
                                                    """,
                                'debian': """   DEBIAN
                                                <br /><br />
                                                Debian es un sistema operativo gratuito, una de las distribuciones de 
                                                Linux más populares e influyentes.<br />
                                                <br />
                                                Debian es conocido por su adhesión a las filosofías del software 
                                                libre y por su abundancia de opciones (su actual versión incluye 
                                                más de 18 mil paquetes de software, para once arquitecturas de 
                                                computadora).<br />
                                                <br />
                                                Debian GNU/Linux, también es base para otras múltiples 
                                                distribuciones de Linux como Knoppix, Linspire, MEPIS, Xandros y la 
                                                familia Ubuntu.<br />
                                                <br />
                                                Debian también es conocido por su sistema de gestión de paquetes 
                                                (especialmente APT), por sus estrictas políticas con respecto a sus 
                                                paquetes y la calidad de sus lanzamientos. Estas prácticas permiten 
                                                fáciles actualizaciones entre lanzamientos, y una instalación y 
                                                removión sencilla de paquetes.<br />
                                                <br />
                                                También utiliza un desarrollo y proceso de testeo abiertos. Es 
                                                desarrollado por voluntarios de todo el mundo, y apoyado por 
                                                donaciones a través de la "Software in the Public Interest", 
                                                una organización sin fines de lucro para el apoyo de proyectos 
                                                de software libre.
                                                    """,
                                'ubuntu': """   UBUNTU
                                                <br /><br />
                                                Ubuntu GNU/Linux es un sistema operativo basado en el núcleo Linux y 
                                                en algunas herramientas del Proyecto GNU. <br />
                                                <br />
                                                La estructura técnica del 
                                                sistema está basada en el Proyecto Debian, pero el planteamiento 
                                                está inspirado en los principios de la corriente ubuntu, un 
                                                movimiento humanista encabezado por el obispo Desmond Tutu, 
                                                Premio Nobel de la Paz 1984. <br />
                                                <br />
                                                Económicamente el proyecto se 
                                                sostiene con aportaciones de la empresa Canonical del millonario 
                                                sudafricano Mark Shuttleworth.""",
                                'arch': """ ARCH
                                                <br /><br />
                                                Arch Linux es una distribución desarrollada por la comunidad en forma 
                                                independiente y optimizada para i686/x86-64, basada en un modo de 
                                                liberado continuo y dirigida a usuarios con un nivel intermedio y 
                                                avanzado. Ofrece un gran repositorio con binarios y un excelente 
                                                gestor de paquetes, así como un sistema de paquetes parecido a los 
                                                ports. El desarrollo se centra sobre un balance de minimalismo, 
                                                elegancia, correcciones de código y modernidad.
                                                <br /><br />
                                                Está basadá originalmente en las ideas de CRUX, una gran 
                                                distribución desarrollada por Per Lidén. La versión 0.1 
                                                (Homero) de Arch Linux fue lanzada el 11 de marzo de 2002.
                                                <br /><br />
                                                Arch provee un entorno mínimo después de la instalación (sin GUI), 
                                                compilado para arquitecturas i686/x86-64. Arch es ligera, flexible, 
                                                rápida, simple y apunta a ser muy similar a UNIX. Su diseño, 
                                                filosofía e implementación hace fácil extenderla y moldearla a 
                                                cualquier tipo de sistema que estés construyendo: desde una 
                                                máquina de consola minimalista al más grandioso entorno de 
                                                escritorio habilitado con ricas características. 
                                                <br /><br />
                                                En lugar de arrancar paquetes innecesarios y no deseados Arch ofrece, 
                                                al usuario, el poder y la capacidad para construir desde una base 
                                                mínima sin ninguna opción por defecto. El usuario es quién decide 
                                                que Arch Linux instalará.
                                                    """,
                                'gentoo': """GENTOO
                                                <br /><br />
                                                Gentoo Linux es una distribución GNU/Linux orientada a usuarios con 
                                                cierta experiencia en este sistema operativo, fue fundada por 
                                                Daniel Robbins, basada en la inactiva distribución llamada Enoch 
                                                Linux. 
                                                <br /><br />
                                                Ya para el año 2002, ésta última pasa a denominarse Gentoo Linux.
                                                <br /><br />
                                                El nombre Gentoo proviene del nombre en inglés del pingüino papúa. 
                                                Nótese que la mascota de Linux es un pingüino.
                                                <br /><br />
                                                La piedra angular de Gentoo es Portage, un sistema de distribución 
                                                de software basado en Ports de BSD. Portage consiste en un árbol 
                                                local, que contiene las descripciones de los paquetes de software, 
                                                así como los scripts necesarios para instalarlos. 
                                                <br /><br />
                                                Este árbol se puede sincronizar con un servidor remoto mediante una orden.
                                                """,
                                'centos': """CENTOS
                                            <br /><br />
                                            CentOS (acrónimo de Community ENTerprise Operating System) es un 
                                            clon a nivel binario de la distribución Red Hat Enterprise Linux, 
                                            compilado por voluntarios a partir del código fuente liberado por 
                                            Red Hat, empresa desarrolladora de RHEL.
                                            <br /><br />
                                            Red Hat Enterprise Linux se compone de software libre y código 
                                            abierto, pero se publica en formato binario usable (CD-ROM o DVD-ROM) 
                                            solamente a suscriptores pagados. 
                                            <br /><br />
                                            Como es requerido, Red Hat libera 
                                            todo el código fuente del producto de forma pública bajo los términos 
                                            de la Licencia Pública GNU y otras licencias. Los desarrolladores de 
                                            CentOS usan ese código fuente para crear un producto final que es 
                                            muy similar al Red Hat Enterprise Linux y está libremente disponible 
                                            para ser bajado y usado por el público, pero no es mantenido ni 
                                            soportado por Red Hat. 
                                            <br /><br />
                                            Existen otras distribuciones también 
                                            derivadas de los fuentes de Red Hat.
                                            <br /><br />
                                            CentOS usa yum para bajar e instalar las actualizaciones, 
                                            herramienta también utilizada por Fedora Core.
                                            """,
                         },
                        },
                    }
        
        