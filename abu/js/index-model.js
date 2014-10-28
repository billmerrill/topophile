			// var //container, stats;
            var stats;

			var camera, cameraTarget, scene, renderer;
            

			init();
			animate();

			function init() {

				// container = document.createElement( 'div' );
				// document.body.appendChild( container );

                var cameraAspectRatio = $("#model").width()/$("#model").height();
				camera = new THREE.PerspectiveCamera(35, cameraAspectRatio, 1, 500 );
				camera.position.set( 130, -40, 70 );

				cameraTarget = new THREE.Vector3( 20, 20, 0 );

				scene = new THREE.Scene();


				// Binary files

				var material = new THREE.MeshPhongMaterial( { ambient: 0x555555, color: 0xAAAAAA, specular: 0x111111, shininess: 200 } );

				var loader = new THREE.STLLoader();
				loader.addEventListener( 'load', function ( event ) {

					var geometry = event.content;
					var mesh = new THREE.Mesh( geometry, material );

					mesh.castShadow = true;
					mesh.receiveShadow = true;

					scene.add( mesh );

				} );
				loader.load( './assets/rainier.stl' );


				// Lights

				scene.add( new THREE.AmbientLight( 0x777777 ) );

				addShadowedLight( 1, 1, 1, 0xffffff, 1.35 );
				addShadowedLight( 0.5, 1, -1, 0xffaa00, 1 );

				// renderer

				renderer = new THREE.WebGLRenderer( { antialias: true } );
				renderer.setSize( $('#model-container').width(), $('#model-container').height() );

				// renderer.setClearColor( scene.fog.color, 1 );

				renderer.gammaInput = true;
				renderer.gammaOutput = true;

				renderer.shadowMapEnabled = true;
				renderer.shadowMapCullFace = THREE.CullFaceBack;

				// container.appendChild( renderer.domElement );
                modelContainer = $("#model-container");
                var mC = document.getElementById("model-container");

                var pageModel = document.getElementById("model");
                mC.replaceChild(renderer.domElement, pageModel);

				// stats

				// stats = new Stats();
				// stats.domElement.style.position = 'absolute';
				// stats.domElement.style.top = '0px';
				// modelContainer.appendChild( stats.domElement );

				//

				window.addEventListener( 'resize', onWindowResize, false );

			}

			function addShadowedLight( x, y, z, color, intensity ) {

				var directionalLight = new THREE.DirectionalLight( color, intensity );
				directionalLight.position.set( x, y, z )
				scene.add( directionalLight );

				directionalLight.castShadow = true;
				// directionalLight.shadowCameraVisible = true;

				var d = 1;
				directionalLight.shadowCameraLeft = -d;
				directionalLight.shadowCameraRight = d;
				directionalLight.shadowCameraTop = d;
				directionalLight.shadowCameraBottom = -d;

				directionalLight.shadowCameraNear = 1;
				directionalLight.shadowCameraFar = 4;

				directionalLight.shadowMapWidth = 1024;
				directionalLight.shadowMapHeight = 1024;

				directionalLight.shadowBias = -0.005;
				directionalLight.shadowDarkness = 0.15;

			}

			function onWindowResize() {

				// camera.aspect = window.innerWidth / window.innerHeight;
                camera.aspect = $("#model").width()/$("#model").height();
				camera.updateProjectionMatrix();

				// renderer.setSize( window.innerWidth, window.innerHeight );
				renderer.setSize( $("#model").width(), $("#model").height() );

			}

			function animate() {

				requestAnimationFrame( animate );

				render();
				// stats.update();

			}

			function render() {

				// var timer = Date.now() * 0.0005;

				// camera.position.x = Math.cos( timer ) * 3;
				// camera.position.z = Math.sin( timer ) * 3;
                
                camera.up = new THREE.Vector3(0,0,1);
				camera.lookAt( cameraTarget );

				renderer.render( scene, camera );
                

			}