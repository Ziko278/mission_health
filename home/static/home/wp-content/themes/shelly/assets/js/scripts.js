/**
 * Shelly
 * Shelly is an attractive minimal WordPress theme for different types of education centers
 * Exclusively on https://1.envato.market/shelly
 *
 * @encoding        UTF-8
 * @version         {{plugin_version}}
 * @copyright       (C) 2018 - 2021 Merkulove ( https://merkulov.design/ ). All rights reserved.
 * @license         Envato License https://1.envato.market/KYbje
 * @contributors    Dmitry Merkulov (dmitry@merkulov.design)
 * @support         help@merkulov.design
 **/

jQuery( document ).ready( function( $ ) {

    "use strict";

    let tiltSettings = [];
    const burgerMenuTrigger = 991;

    /**
     * Init tilt effect
     *
     * @param wrapper
     * @param elements
     */
    function initTilt( wrapper, elements ) {

        const $wrapper = $( wrapper );
        const $elements = $( elements );
        if ( $wrapper.length < 1 || $elements.length < 1 ) { return; }

        /** Init TweenMax  */
        TweenMax.set( [ $elements ], { transformStyle: "preserve-3d" } );

        /** Add event listeners fot tilt effect */
        $wrapper.mousemove( ( e ) => {

            tilt( e.pageX, e.pageY, $wrapper, $elements );

        } );

        /** Add event listeners fot mouse left */
        $wrapper.mouseleave( ( e ) => {

            tilt( $wrapper.width() / 2, $wrapper.height() / 2, $wrapper, $elements );

        } );

    }

    /**
     * Shelly tilt
     *
     * @param cx
     * @param cy
     * @param $wrapper
     * @param $elements
     */
    function tilt( cx, cy, $wrapper, $elements ) {

        const sxPos = ( cx / $wrapper.width() * 100 - 50 ) * 2 ;
        const syPos = ( cy / $wrapper.height() * 100 - 50 ) * 2;
        let elementsCounter = 0;

        /** Separate animation for each element */
        for ( const $element of $elements ) {

            /** Set random tilt multiplier */
            if ( tiltSettings[ elementsCounter ] === undefined ) {

                tiltSettings[ elementsCounter ] = Math.floor(Math.random() * 25 ) * 0.01;

            }

            /** Apply effect */
            TweenMax.to( $element, 2, {

                rotationY: -tiltSettings[ elementsCounter ] * sxPos,
                rotationX: tiltSettings[ elementsCounter ] * syPos,
                transformPerspective: 500,
                transformOrigin: "center center 200",
                ease: Expo.easeOut

            });

            elementsCounter++;

        }

    }

    /**
     * Burger menu handler
     */
    function initBurgerMenu() {

        const value = jQuery(window).width(); // New width

        if ( value > burgerMenuTrigger ) {
            jQuery(".responsive-menu").removeClass("active");
            jQuery(".responsive-menu-btn").removeClass("active");

        }

    }

    /**
     * Burger menu button click handler
     */
    function openBurgerMenu() {

        jQuery( this ).toggleClass( 'active' );
        jQuery( '.responsive-menu' ).toggleClass( 'active' );
        jQuery( 'body' ).toggleClass( 'scroll-hide' );

    }

    /**
     * Open child level for submenu in responsive menu
     */
    function openMenuChild() {

        jQuery( this ).toggleClass( 'expand' )
        jQuery( this ).parent().toggleClass( 'active' ).siblings().removeClass( 'active' );
        jQuery( this ).next( 'ul' ).slideToggle();

    }

    /**
     * Init responsive menu
     */
    function initMenu() {

        jQuery( window ).on("resize",initBurgerMenu );
        jQuery( '.responsive-menu-btn' ).on("click", openBurgerMenu );

        jQuery( '.responsive-menu ul ul' ).parent().addClass( 'menu-item-has-children' );
        jQuery( '.responsive-menu ul li.menu-item-has-children > a' ).after( '<span class="dropdown-icon"><i class="fas fa-angle-down"></i></span>' );
        jQuery( '.responsive-menu ul li.menu-item-has-children ul.sub-menu').hide();
        jQuery( '.responsive-menu ul li.menu-item-has-children').next( 'ul' ).css( 'display', 'none' );
        jQuery( '.responsive-menu ul li.menu-item-has-children > .dropdown-icon ').on( 'click', openMenuChild );

    }

    jQuery('.blog-carousel').slick({
        slidesToShow: 1,
        infinite:true,
        slidesToScroll: 1,
        autoplay: true,
        dots: false,
        arrows:true,
        autoplaySpeed: 2000
    });

    /**
     * Reply button for comments form
     * @type {jQuery|HTMLElement|*}
     */
    const $replyLink = $('.comment-reply-link');
    const $respondForm = $('#respond textarea[name="comment"]');

	if ( $replyLink.length ) {
        $replyLink.on('click', function( e ) {
			setTimeout( function() {
				$('html, body').animate({
					scrollTop: $respondForm.offset().top - 500
				}, 250 );
                $respondForm.focus();
			}, 200 );
		});
	}
	
    $('.wrk-list').slick({
        slidesToShow: 5,
        slidesToScroll: 1,
        dots: false,
        arrows: false,
        infinite:true,
        centerPadding: "40px",
        centerMode: true,
        focusOnSelect: true,
        asNavFor: '.slider-content',
        responsive: [
            {
                breakpoint: 991,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1
                }
            },
            {
                breakpoint: 576,
                settings: {
                    slidesToShow: 1
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });

    jQuery(".classes-widget-slider").slick({
        slidesToShow:1,
        infinite:!0,
        slidesToScroll:1,
        autoplay:!0,
        dots:!0,
        arrows:!1,
        autoplaySpeed:2e3
    });
    
    $('.slider-content').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        dots: true,
        arrows: true,
        asNavFor: '.wrk-list',
        centerMode: false,
        focusOnSelect: true
    });

    if ($(window).width() < 768) {
        $('.data-list').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: false,
            arrows: true,
            asNavFor: '.tabs-content',
            centerMode: false,
            focusOnSelect: true,
            infinite:false
        });

        $('.tabs-content').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: true,
            arrows: false,
            infinite:false,
            asNavFor: '.data-list',
            centerMode: false,
            focusOnSelect: true
        });
    }

    initMenu();

    initTilt( 'body', '.color-accent-motion' );

});