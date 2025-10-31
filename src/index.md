---
layout: home.njk
title: Maja Explosiv
description: Contemporary artist exploring the intersection of art and design through various mediums
showPageTitle: false
showFeaturedPosts: false
showFeaturedCollections: false
hero:
  title: Maja Explosiv
  subtitle: Contemporary Artist
  description: |
    <p>Exploring the intersection of art and design through various mediums.</p>
  backgroundImage: /assets/images/hero/hero-maja-explosiv.jpg
  ctaButton:
    text: Explore Works
    url: /#projects
carousels:
  hero:
    autoplay: true
    interval: 5000
    showDots: true
    showArrows: true
    height: 500px
    images:
      - src: /assets/images/carousel/hero/maja-explosiv-hero1.jpg
        alt: Abstract painting by Maja Explosiv
        title: Paintings
        caption: Explore expressive paintings and murals
        link: /collections/paintings/
      - src: /assets/images/carousel/hero/maja-explosiv-hero2.jpg
        alt: Sculpture by Maja Explosiv
        title: Sculptures
        caption: Discover intricate three-dimensional creations
        link: /collections/sculptures/
      - src: /assets/images/carousel/hero/maja-explosiv-hero3.jpg
        alt: Art installation by Maja Explosiv
        title: Installations
        caption: Experience immersive art installations
        link: /collections/installations/
customSections:
  - title: Projects
    class: projects-section
    id: projects
    content: |
      <div class="projects-tabs">
        <div class="tab-buttons">
          <button class="tab-button active" data-tab="sculptures">Sculptures</button>
          <button class="tab-button" data-tab="installations">Installations</button>
          <button class="tab-button" data-tab="performance">Performance</button>
          <button class="tab-button" data-tab="paintings">Paintings</button>
        </div>
        <div class="tab-content">
          <div id="sculptures" class="tab-pane active">
            <p>Sculptural works exploring form, space, and materiality.</p>
          </div>
          <div id="installations" class="tab-pane">
            <p>Large-scale installations that transform and engage with their environment.</p>
          </div>
          <div id="performance" class="tab-pane">
            <p>Performance art and multimedia events.</p>
          </div>
          <div id="paintings" class="tab-pane">
            <p>Paintings, murals, and works on paper.</p>
          </div>
        </div>
      </div>
  - title: About
    class: about-section
    id: about
    content: |
      <div class="about-tabs">
        <div class="tab-buttons">
          <button class="tab-button active" data-tab="bio">Bio</button>
          <button class="tab-button" data-tab="press">Press</button>
          <button class="tab-button" data-tab="links">Links</button>
        </div>
        <div class="tab-content">
          <div id="bio" class="tab-pane active">
            <p>Maja Explosiv is a multidisciplinary artist known for her bold and experimental approach to art. Her work often challenges conventional boundaries, blending traditional techniques with contemporary themes.</p>
            <p>With a background in fine arts and a passion for innovation, Maja's creations invite viewers to engage in a dialogue about society, nature, and the human experience.</p>
          </div>
          <div id="press" class="tab-pane">
            <p>Press information and media coverage.</p>
          </div>
          <div id="links" class="tab-pane">
            <p>Links and resources.</p>
          </div>
        </div>
      </div>
---

{% carousel "hero" %}
