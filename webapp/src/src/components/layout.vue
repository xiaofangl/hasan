<template>
  <div>
    <slot name="header">
      <hs-header></hs-header>
    </slot>
    <slot name="sidebar">
      <hs-sidebar></hs-sidebar>
    </slot>
    <div id="main">
      <div id="content">
        <div class="maincontent">
          <slot></slot>
        </div>
      </div>
    </div>
    <slot name="footer-dialog"></slot>
  </div>
</template>

