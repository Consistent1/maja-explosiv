---
layout: home.njk
title: Maja Explosiv
description: Contemporary artist exploring the intersection of art and design through various mediums
showPageTitle: false
showFeaturedPosts: false
showFeaturedCollections: false
hero:
  title: MAJA
  subtitle: EXPLOSIV
  description: |
    <p>Multidisciplinary artist whose extensive oeuvre includes metal work, illustration, painting, theatre development and project management.</p>
    <p>For commissions, collaborations or bookings reach out to us.</p>
  ctaButton:
    text: LETS GET IN TOUCH
    url: "#contact"
# carousels:
#   hero:
#     autoplay: true
#     interval: 5000
#     showDots: true
#     showArrows: true
#     height: 500px
#     images:
#       - src: /assets/images/carousel/hero/maja-explosiv-hero1.jpg
#         alt: Abstract painting by Maja Explosiv
#         title: Paintings
#         caption: Explore expressive paintings and murals
#         link: /collections/paintings/
#       - src: /assets/images/carousel/hero/maja-explosiv-hero2.jpg
#         alt: Sculpture by Maja Explosiv
#         title: Sculptures
#         caption: Discover intricate three-dimensional creations
#         link: /collections/sculptures/
#       - src: /assets/images/carousel/hero/maja-explosiv-hero3.jpg
#         alt: Art installation by Maja Explosiv
#         title: Installations
#         caption: Experience immersive art installations
#         link: /collections/installations/
customSections:
  - title: Projects
    class: projects-section
    id: projects
    content: |
      <div class="projects-tabs" aria-labelledby="projects-tabs-label">
        <div class="tab-buttons" role="tablist" aria-label="Projects">
          <button role="tab" aria-selected="true" aria-controls="sculptures" id="tab-sculptures" class="tab-button" data-tab="sculptures">Sculptures</button>
          <button role="tab" aria-selected="false" aria-controls="installations" id="tab-installations" class="tab-button" data-tab="installations">Installations</button>
          <button role="tab" aria-selected="false" aria-controls="performance" id="tab-performance" class="tab-button" data-tab="performance">Performance</button>
          <button role="tab" aria-selected="false" aria-controls="paintings" id="tab-paintings" class="tab-button" data-tab="paintings">Paintings</button>
        </div>
        <div class="tab-content">
          <div id="sculptures" role="tabpanel" aria-labelledby="tab-sculptures" aria-hidden="false" class="tab-pane active">
            <p>Sculptural works exploring form, space, and materiality.</p>
          </div>
          <div id="installations" role="tabpanel" aria-labelledby="tab-installations" aria-hidden="true" class="tab-pane">
            <p>Large-scale installations that transform and engage with their environment.</p>
          </div>
          <div id="performance" role="tabpanel" aria-labelledby="tab-performance" aria-hidden="true" class="tab-pane">
            <p>Performance art and multimedia events.</p>
          </div>
          <div id="paintings" role="tabpanel" aria-labelledby="tab-paintings" aria-hidden="true" class="tab-pane">
            <p>Paintings, murals, and works on paper.</p>
          </div>
        </div>
      </div>
  - title: About
    class: about-section
    id: about
    content: |
      <div class="about-tabs" aria-labelledby="about-tabs-label">
        <div class="tab-buttons" role="tablist" aria-label="About">
          <button role="tab" aria-selected="true" aria-controls="bio" id="tab-bio" class="tab-button" data-tab="bio">Bio</button>
          <button role="tab" aria-selected="false" aria-controls="timeline" id="tab-timeline" class="tab-button" data-tab="timeline">Timeline</button>
          <button role="tab" aria-selected="false" aria-controls="press" id="tab-press" class="tab-button" data-tab="press">Press</button>
          <button role="tab" aria-selected="false" aria-controls="links" id="tab-links" class="tab-button" data-tab="links">Links</button>
        </div>
        <div class="tab-content">
          <div id="bio" role="tabpanel" aria-labelledby="tab-bio" aria-hidden="false" class="tab-pane active">
            <p>Maja Explosiv is a multidisciplinary artist known for her bold and experimental approach to art. Her work often challenges conventional boundaries, blending traditional techniques with contemporary themes.</p>
            <p>With a background in fine arts and a passion for innovation, Maja's creations invite viewers to engage in a dialogue about society, nature, and the human experience.</p>
          </div>
          <div id="timeline" role="tabpanel" aria-labelledby="tab-timeline" aria-hidden="true" class="tab-pane">
            <p>Timeline of exhibitions and milestones.</p>
          </div>
          <div id="press" role="tabpanel" aria-labelledby="tab-press" aria-hidden="true" class="tab-pane">
            <p>Press information and media coverage.</p>
          </div>
          <div id="links" role="tabpanel" aria-labelledby="tab-links" aria-hidden="true" class="tab-pane">
            <p>Links and resources.</p>
          </div>
        </div>
      </div>
---
