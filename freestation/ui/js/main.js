"use strict"; 

var content_selected = []

function hello() 
{
    var couch_server = new couch.Server();
    $A('hello').textContent = 'Demo is talking to CouchDB ' + couch_server.get_sync()['version'];
    
    Hub.send('loaded', 'test');
}
    
function on_main_button_click(button)
{
	console.log('Pressed ' + button)
}

function on_press_copy_usb()
{
	//alert('copy usb')
	var usb_status = $('usb_status').get('text')
	
	if(usb_status == 'No')
	{
		$('copyusb_message').set('text', 'Por favor introduce un USB')
	}
	else
	{
		if(content_selected.length <= 0)
		{
			$('copyusb_message').set('text', 'Es necesario seleccionar algun elemento')
		}
		else
		{
			$('copyusb_message').set('text', 'Espera por favor, copiando datos');
			
			(function() 
		    {
		        Hub.send('copyusb', content_selected)
		    }).delay(1500);
		}
	}
}

function on_press_distributions()
{
	var vertical_slide_left = new Fx.Slide('sidebar_left_container');
	var vertical_slide_right = new Fx.Slide('sidebar_right_container');
	    
    vertical_slide_left.slideOut();
    vertical_slide_right.slideOut();
    //$('sidebar_left_container').empty()
            
    $('status_page').set('html', '<img style="margin-left:100px;" src="img/arrow.png"> <img style="margin-left:10px;height:75px" src="http://freestation.quijost.com/img/client/distributions-button.png" title="Distribution">'); //empty()
            
    (function() 
    {
        Hub.send('on_fs_request', 'distribution', 'left')
    }).delay(1500);
    
    (function() 
    {
        Hub.send('on_fs_request', 'right_description', 'right')
    }).delay(1500);
            
    }

function on_press_software()
{
    var vertical_slide_left = new Fx.Slide('sidebar_left_container');
    var vertical_slide_right = new Fx.Slide('sidebar_right_container');
        
    vertical_slide_left.slideOut();
    vertical_slide_right.slideOut();
    //$('sidebar_left_container').empty()
            
    $('status_page').set('html', '<img style="margin-left:100px;" src="img/arrow.png"> <img style="margin-left:10px;height:75px" src="http://freestation.quijost.com/img/client/software-button.png" title="Software">'); //empty()
            
    (function() 
    {
        Hub.send('on_fs_request', 'software', 'left')
    }).delay(1500);
    
    (function() 
    {
        Hub.send('on_fs_request', 'right_description', 'right')
    }).delay(1500);
}

function on_press_documentation()
{
    var vertical_slide_left = new Fx.Slide('sidebar_left_container');
    var vertical_slide_right = new Fx.Slide('sidebar_right_container');
        
    vertical_slide_left.slideOut();
    vertical_slide_right.slideOut();
    //$('sidebar_left_container').empty()
            
    $('status_page').set('html', '<img style="margin-left:100px;" src="img/arrow.png">  <img style="margin-left:10px;height:75px" src="http://freestation.quijost.com/img/client/documentation-button.png" title="Documentation">'); //empty()
            
    (function() 
    {
        Hub.send('on_fs_request', 'documentation', 'left')
    }).delay(1500);
    
    (function() 
    {
        Hub.send('on_fs_request', 'right_description', 'right')
    }).delay(1500);
}

function on_press_resources()
{
    var vertical_slide_left = new Fx.Slide('sidebar_left_container');
    var vertical_slide_right = new Fx.Slide('sidebar_right_container');
        
    vertical_slide_left.slideOut();
    vertical_slide_right.slideOut();
    //$('sidebar_left_container').empty()
            
    $('status_page').set('html', '<img style="margin-left:100px;" src="img/arrow.png"> <img style="margin-left:10px;height:75px" src="http://freestation.quijost.com/img/client/resources-button.png" title="Resources">'); //empty()
            
    (function() 
    {
        Hub.send('on_fs_request', 'resources', 'left')
    }).delay(1500);
    
    (function() 
    {
        Hub.send('on_fs_request', 'right_description', 'right')
    }).delay(1500);
}

Hub.connect('updater_description',
        function(data) 
        {
            $('description_content').empty().set('html', data); //
        }
    );

Hub.connect('copyusb_finished',
        function() 
        {
			usb_data = []
			$('copyusb_message').set('text', '¡Datos copiados correctamente!')
			$('bar').setStyle('display', 'none')
        }
    );

var usb_data = []
Hub.connect('mount_added',
        function(name, total_size, capacity, percent) 
        {
            console.log('mount_added')
            var usb_status = $('usb_status').set('text', 'Yes')
            usb_data['name'] = name
            usb_data['total_size'] = total_size
            usb_data['capacity'] = capacity
            usb_data['capacity'] = percent
            
            $('usb_info').set('html', 'Almacenamiento USB: ' + name + ' Tamaño: ' + capacity + ' Espacio libre: ' + total_size)
            $('bar').setStyle('display', 'block')
            $('bar').set('value', percent)
        }
    );

function get_description(data)
{
	Hub.send('on_get_description', data)
	
	if(!$(data + '_status').get('text'))
	{
		$(data + '_status').set('text', 'Seleccionado')
		$(data + '_status').removeClass('unselected_box')
		$(data + '_status').addClass('selected_box')
		content_selected.push(data)
	}
	else
	{
		//content_selected.remove(data)
		$(data + '_status').set('text', '')
		$(data + '_status').removeClass('selected_box')
		$(data + '_status').addClass('unselected_box')
	}
	
	console.log(content_selected)
}


window.addEvent('domready', function()
{
	console.log('domready enabled')
	
	var vertical_slide_left = new Fx.Slide('sidebar_left_container');
	var vertical_slide_right = new Fx.Slide('sidebar_right_container');
	
	Hub.connect('updater',
		    function(data, side) 
		    {
		       if(side == 'left')
		       {
		    	   vertical_slide_left.slideIn();
		    	   $('sidebar_' + side + '_container').set('html', data); //empty()
		       }
		       else if(side == 'right')
		       {
		    	   vertical_slide_right.slideIn();
		    	   $('sidebar_' + side + '_container').set('html', data); //empty()
		       }
		       else if(side == 'home')
               {
		    	   vertical_slide_left.slideIn();
                   $('sidebar_left_container').set('html', data); //empty()
               }
		       
		    }
		);
	
	$('home_button').addEvent('click', function(event)
    {
		event.stop();
		$('status_page').empty()
        vertical_slide_left.slideOut();
        vertical_slide_right.slideOut();
        
        (function() {
            Hub.send('on_fs_request', 'home', 'home')
        }).delay(1500);
        
        (function() {
            Hub.send('on_fs_request', 'home_news', 'right')
        }).delay(1500);
        
        window.fireEvent('domready');
        console.log('desde home button')
    })
    
    if ($('software_button'))
    {
		$('software_button').addEvent('click', function(event)
		{
			event.stop();
			on_press_software()
		})
    }
    if ($('distributions_button'))
    {
        $('distributions_button').addEvent('click', function(event)
        {
            event.stop();
            on_press_distributions()
        })
    }
})