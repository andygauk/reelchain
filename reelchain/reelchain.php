<?php
/**
 * Plugin Name: ReelChain
 * Description: Embed the ReelChain film-to-film actor-bridge puzzle game via the [reelchain] shortcode (or the reelchain_game() template tag).
 * Version: 1.0.0
 * Author: ReelChain
 */

if ( ! defined( 'ABSPATH' ) ) exit;

// Enqueue the game's CSS + JS (external files -> never touched by WP filters).
function reelchain_enqueue_assets() {
    $css = plugins_url( 'assets/reelchain.css', __FILE__ );
    $js  = plugins_url( 'assets/reelchain.js',  __FILE__ );
    wp_enqueue_style(  'reelchain', $css, array(), '1.0.0' );
    wp_enqueue_script( 'reelchain', $js,  array(), '1.0.0', true );
}

// Only load the assets on pages that actually use the shortcode.
function reelchain_maybe_enqueue() {
    if ( is_singular() && has_shortcode( get_post()->post_content, 'reelchain' ) ) {
        reelchain_enqueue_assets();
    }
}
add_action( 'wp_enqueue_scripts', 'reelchain_maybe_enqueue' );

// Shortcode: [reelchain]  -> paste into a page in the block editor.
function reelchain_shortcode() {
    $file = __DIR__ . '/assets/reelchain-markup.html';
    if ( ! file_exists( $file ) ) {
        return '<!-- ReelChain: game markup not found. Re-run build_game.py. -->';
    }
    return file_get_contents( $file );
}
add_shortcode( 'reelchain', 'reelchain_shortcode' );

// Template tag: call reelchain_game() directly in a theme template
// (e.g. inside page-reelchain.php).
function reelchain_game() {
    reelchain_enqueue_assets();
    $file = __DIR__ . '/assets/reelchain-markup.html';
    if ( file_exists( $file ) ) {
        echo file_get_contents( $file );
    }
}
