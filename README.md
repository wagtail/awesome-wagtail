# Awesome Wagtail [![Awesome](https://cdn.jsdelivr.net/gh/sindresorhus/awesome@d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome) [<img src="https://cdn.jsdelivr.net/gh/wagtail/awesome-wagtail@ac912cc661a7099813f90545adffa6bb3e75216c/logo.svg" width="104" align="right" alt="Wagtail">](https://wagtail.org/)

> A curated list of awesome packages, articles, and other cool resources from the Wagtail community.
> [Wagtail](https://wagtail.org/) is a Python CMS powered by Django, focusing on flexibility and user experience.

_You might also like [Awesome Django](https://github.com/wsvincent/awesome-django) and [Awesome Python](https://github.com/vinta/awesome-python). :snake:_

## Contents

- [General resources](#general-resources)
- [Apps](#apps)
  - [Blogging/news](#bloggingnews)
  - [Rich text editor extensions](#rich-text-editor-extensions)
  - [Widgets](#widgets)
  - [StreamField](#streamfield)
  - [Static site generation](#static-site-generation)
  - [Settings management](#settings-management)
  - [E-commerce](#e-commerce)
  - [SEO and SMO](#seo-and-smo)
  - [Customer experience](#customer-experience)
  - [Security](#security)
  - [Media](#media)
  - [Translations](#translations)
  - [Forms](#forms)
  - [Testing](#testing)
  - [Modeladmin](#modeladmin)
  - [Content Management](#content-management)
  - [Misc](#misc)
- [Tools](#tools)
  - [Templates & Starter Kits](#templates--starter-kits)
- [Resources](#resources)
  - [Getting started](#getting-started)
  - [Articles](#articles)
  - [Presentations](#presentations)
  - [Podcasts](#podcasts)
  - [Videos](#videos)
  - [Showcases](#showcases)
  - [Package lists](#package-lists)
- [Documentation for editors](#documentation-for-editors)
- [Community](#community)
- [Open-source sites](#open-source-sites)

## General resources

- [Official site](https://wagtail.org/)
- [Code repository](https://github.com/wagtail/wagtail)
- [Official demo](https://github.com/wagtail/bakerydemo)
- [User guide](https://guide.wagtail.org/)
- [Developer docs](https://docs.wagtail.org/)
- [Project roadmap](https://wagtail.org/roadmap/)

## Apps

### Blogging/news

- [Wagtail CRX (CodeRed Extensions)](https://github.com/coderedcorp/coderedcms) - Wagtail + CodeRed Extensions enabling rapid development of marketing-focused websites.
- [Puput](https://github.com/APSL/puput) - A Django blog app implemented in Wagtail.
- [Commentail](https://github.com/hardcodd/Commentail) - Self-hosted comments for Wagtail CMS with built-in moderation, email-verified guests, threaded replies and email notifications. No external comments service required.

### Rich text editor extensions

- [Wagtail EditorJS](https://github.com/Nigel2392/wagtail_editorjs) - EditorJS Wagtail widget with page, document and image- chooser functionality. Use Wagtail blocks in your richtext.
- [Wagtail Terms](https://github.com/smark-1/wagtailterms) - A Wagtail plugin to add support for glossary terms entity to Draftail.

### Widgets

- [wagtailgmaps](https://github.com/springload/wagtailgmaps) - Simple Google Maps address formatter for Wagtail fields.
- [Wagtail-Geo-Widget](https://github.com/Frojd/wagtail-geo-widget) - Wagtail-Geo-Widget is the complete map solution for your Wagtail site.
- [wagtail-markdown](https://github.com/torchbox/wagtail-markdown) - Markdown support for Wagtail.
- [wagtail-autocomplete](https://github.com/wagtail/wagtail-autocomplete) - An Autocomplete edit handler for selecting Pages, Snippets, and more.
- [wagtail-instance-selector](https://github.com/ixc/wagtail-instance-selector) - A widget for Wagtail's admin that allows you to create and select related items.
- [wagtail-generic-chooser](https://github.com/wagtail/wagtail-generic-chooser) - A toolkit for custom chooser popups in Wagtail.
- [Wagtail-Color-Panel](https://github.com/marteinn/wagtail-color-panel) - A package that adds new panels for selecting colors, works both on regular page fields and stream field.
- [wagtail-html-editor](https://github.com/kkm-horikawa/wagtail-html-editor) - Enhanced HTML editor block for Wagtail CMS with CodeMirror 6, syntax highlighting, Emmet support, and fullscreen mode.

### StreamField

- [wagtail-inventory](https://github.com/cfpb/wagtail-inventory) - Search Wagtail pages by the StreamField blocks they contain.
- [Wagtail Code Block](https://github.com/wagtail-nest/wagtailcodeblock) - StreamField code blocks for the Wagtail CMS with real-time PrismJS Syntax Highlighting.

### Static site generation

- [Wagtail-bakery](https://github.com/wagtail-nest/wagtail-bakery) - A set of helpers for baking your Django Wagtail site out as flat files.

### Settings management

- [Wagtail-Flags](https://github.com/cfpb/wagtail-flags) - Feature flags for Wagtail sites.

### E-commerce

- [django-salesman](https://github.com/dinoperovic/django-salesman) - Headless e-commerce framework for Django and Wagtail.

### SEO and SMO

- [wagtail-meta-preview](https://github.com/Frojd/wagtail-meta-preview) - Wagtail Meta Preview provides panels for previewing Facebook sharing, Twitter sharing and Google search results in the Wagtail admin.
- [Wagtail Yoast](https://github.com/Aleksi44/wagtailyoast) - Wagtail + Yoast.
- [Wagtail SEO](https://github.com/coderedcorp/wagtail-seo) - Search engine and social media optimization for Wagtail.

### Customer experience

- [Wagtail Experiments](https://github.com/torchbox/wagtail-experiments) - A/B testing for Wagtail.
- [Wagtail Personalisation](https://github.com/wagtail-nest/wagtail-personalisation) - Rule-based personalisation for Wagtail CMS.

### Security

- [wagtail-2fa](https://github.com/labd/wagtail-2fa) - 2 Factor Authentication for Wagtail.

### Media

- [wagtailmedia](https://github.com/torchbox/wagtailmedia) - A Wagtail module for managing video and audio files within the admin.
- [Wagtail Transcription](https://github.com/j-bodek/wagtail-transcription) - Provides a field to automatically create transcriptions from YouTube videos.

### Translations

- [Wagtail Localize](https://github.com/wagtail/wagtail-localize) - Translation plugin for Wagtail CMS.
- [Wagtail Modeltranslation](https://github.com/infoportugal/wagtail-modeltranslation) - Simple app to patch modeltranslation (https://github.com/deschler/django-modeltranslation) into Wagtail CMS.

### Forms

- [Wagtail's built in Form Builder](https://docs.wagtail.org/en/stable/reference/contrib/forms/) for general use cases.
- [Wagtail ReCaptcha](https://github.com/wagtail-nest/wagtail-django-recaptcha) - A simple recaptcha field for Wagtail Form Pages.
- [Wagtail Jotform](https://github.com/torchbox/wagtail-jotform) - A plugin for using jotforms in wagtail.
- [Wagtail Model Forms](https://github.com/vicktornl/wagtail-model-forms) - The Wagtail Form Builder functionalities available for your models/snippets.
- [Wagtail Formation](https://github.com/mwesterhof/wagtail_formation) - Dynamic forms in wagtail.

### Testing

- [Wagtail Accessibility](https://github.com/wagtail-nest/wagtail-accessibility) - ✅ Accessibility content checks for Wagtail websites.
- [Wagtail Factories](https://github.com/wagtail/wagtail-factories) - Factory boy classes for wagtail.

### Modeladmin

- [wagtail-admin-list-controls](https://github.com/ixc/wagtail-admin-list-controls) - A UI toolkit that extends Wagtail's admin list views and allows you to build custom filters, buttons, panels and more.
- [Wagtail Rangefilter](https://github.com/wunderweiss/wagtail-rangefilter) - Integrates django-admin-rangefilter into Wagtail's ModelAdmin.
- [Wagtail-TreeModelAdmin](https://github.com/cfpb/wagtail-treemodeladmin) - An extension for Wagtail's ModelAdmin for a page explorer-like navigation of Django model relationships.

### Content Management

- [Wagtail Sharing](https://github.com/cfpb/wagtail-sharing) - Easier sharing of Wagtail drafts.
- [Wagtail Transfer](https://github.com/wagtail/wagtail-transfer) - Content transfer for Wagtail.
- [Wagtail Content Import](https://github.com/torchbox/wagtail-content-import) - A module for importing page content into Wagtail from third-party sources. Docs: ...
- [Wagtail Headless Preview](https://github.com/torchbox/wagtail-headless-preview) - Previews for headless Wagtail setups.
- [Wagtail-FEdit](https://github.com/Nigel2392/wagtail_fedit) - Frontend editing on your Wagtail site.

### Misc

- [wagtailmenus](https://github.com/wagtail-nest/wagtailmenus) - An app to help you manage and render menus in your Wagtail projects more effectively.
- [Wagtail Gridder](https://github.com/wharton/wagtailgridder) - Wagtail Gridder is a Bootstrap 4 enabled layout for the Wagtail CMS. Grid Items are created within categories, and displayed on a Grid Index Page. The JavaScript libraries Gridder and MixItUp are included.
- [Wagtail App Pages](https://github.com/mwesterhof/wagtail_app_pages) - Full MVC support for wagtail pages.
- [Wagtail Cache](https://github.com/coderedcorp/wagtail-cache) - A simple page cache for Wagtail based on the Django cache middleware.
- [Wagtail Resume](https://github.com/adinhodovic/wagtail-resume) – A Wagtail project made to simplify creation of resumes for developers.
- [Wagtail Trash](https://github.com/Frojd/wagtail-trash) - Instead of deleting pages when pressing delete, pages will get thrown into the "Trash Can".
- [wagtail-pdf-view](https://github.com/donhauser/wagtail-pdf) - PDF rendering views for the Wagtail CMS.
- [Wagtail Grapple](https://github.com/torchbox/wagtail-grapple) - A Wagtail app that makes building GraphQL endpoints a breeze.
- [wagtail-subscriptions](https://github.com/mojnomiya/wagtail_subscriptions) - A comprehensive subscription management system for Wagtail CMS that provides everything you need to build a SaaS application with subscription billing.

## Tools

### Templates & Starter Kits

- [Pipit](https://github.com/Frojd/Wagtail-Pipit) – Pipit is a Wagtail CMS boilerplate which aims to provide an easy and modern developer workflow with a React-rendered frontend.
- [cookiecutter-wagtail-package](https://github.com/wagtail/cookiecutter-wagtail-package) - A cookiecutter template for building Wagtail add-on packages.
- [Wagtail for Platform.sh](https://github.com/platformsh-templates/wagtail) - Wagtail template for Platform.sh.
- [cookiecutter-wagtail-vix](https://github.com/engineervix/cookiecutter-wagtail-vix) - a minimal, batteries-included, reusable project skeleton to serve as a starting point for a Wagtail project.
- [Sites Conformes](https://github.com/numerique-gouv/sites-conformes) - Gestionnaire de contenu permettant de créer et gérer un site internet basé sur le Système de design de l'État, accessible et sécurisé. Basé sur Wagtail CMS.

### Templates (start command)

- [Wagtail News Template](https://github.com/wagtail/news-template) - A Wagtail template for a news site.

## Resources

### Getting started

<!-- Add new items at the top. Auto-archived after 5 years without updates. -->

- None yet.

### Articles

<!-- Add new items at the top. Auto-archived after 5 years without updates. -->

- [Multi-tenancy with Wagtail](https://cynthiakiser.com/blog/2023/11/01/multitenancy-with-wagtail.html) - Multiple part guide on robust multi-tenancy support in Wagtail. - `2023-11-01`.
- [Wagtail Tutorials: Build Blog Step by Step](https://saashammer.com/blog/wagtail-tutorials/) - The tutorials teach you how to create a standard blog from scratch step by step. - `2023-06-21`.
- [How to Create and Manage Menus of Wagtail application](https://saashammer.com/blog/how-to-create-and-manage-menus-in-wagtail/) - `2023-06-15`.

### Presentations

<!-- Add new items at the top. Auto-archived after 5 years without updates. -->

- [AI in Wagtail: responsible innovation for content editors - Wagtail Space 2025](https://www.youtube.com/watch?v=n2fIFJLSH5E&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=16) by Sage Abdullah and Tom Usher. - `2025-11-19`.
- [Automated Data Loader: Wagtail for Weather Data Integration - Wagtail Space 2025](https://www.youtube.com/watch?v=iTxcq__Gcr4&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=9) by Erick Otenyo and Grace Amondi. - `2025-11-19`.
- [Bird Meets Bot: Using AI Tools to Make Wagtail Smarter - Wagtail Space 2025](https://www.youtube.com/watch?v=SsjXnpuLnL0&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=25) by Alex Tomkins. - `2025-11-19`.
- [Building Better Wagtail Sites: Traits of a Good CMS - Wagtail Space 2025](https://www.youtube.com/watch?v=n5KHTLS22YE&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=5) by Michael Trythall. - `2025-11-19`.
- [Building Flexible Wagtail CMS Experiences for Editors - Wagtail Space 2025](https://www.youtube.com/watch?v=-azqKJdEivk&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=10) by Annette Lewis and Eric Sherman. - `2025-11-19`.
- [Building a little YouTube on Wagtail - Wagtail Space 2025](https://www.youtube.com/watch?v=hLw3FWb2LfQ&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=11) by Tom Dyson. - `2025-11-19`.
- [Code that creates content - Wagtail Space 2025](https://www.youtube.com/watch?v=XkSX195ssjY&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=23) by Alex Morega. - `2025-11-19`.
- [Creating connections between stories and objects using AI - Wagtail Space 2025](https://www.youtube.com/watch?v=Wkjm8xdV_6c&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=12) by Trish Thomas. - `2025-11-19`.
- [Fact checking with Wagtail - Wagtail Space 2025](https://www.youtube.com/watch?v=Spdt-W5XotM&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=21) by Jon Chittenden and Craig Dawson. - `2025-11-19`.
- [Implement the French Government Design System in Wagtail - Wagtail Space 2025](https://www.youtube.com/watch?v=8_CBltGuv0g&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=7) by Sylvain Boissel and Lucie Laporte. - `2025-11-19`.
- [One URL to Rule Them All: Dynamic Landing Pages in Wagtail - Wagtail Space 2025](https://www.youtube.com/watch?v=UOEvu4Lyj8w&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=20) by Chrissy Wainwright and Doug Harris. - `2025-11-19`.
- [REX: Building a SaaS from Wagtail - Wagtail Space 2025](https://www.youtube.com/watch?v=3T-ITKTByH4&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=6) by Sébastien Corbin. - `2025-11-19`.
- [Redesigning and refactoring Wagtail components - Wagtail Space 2025](https://www.youtube.com/watch?v=8h0fxe7b8s8&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=4) by Mariana. - `2025-11-19`.
- [State of Wagtail 2025 - Wagtail Space 2025](https://www.youtube.com/watch?v=9Kduqs6NH7Q&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=2) by Thibaud Colas. - `2025-11-19`.
- [Sympa newsletters with Wagtail - Wagtail Space 2025](https://www.youtube.com/watch?v=n7bM54MAc24&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=22) by Agnès Haasser. - `2025-11-19`.
- [The Bogotá Digital Library: A Wagtail Success Story - Wagtail Space 2025](https://www.youtube.com/watch?v=cbANVWkDIs0&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=17) by Juan Aguayo. - `2025-11-19`.
- [The Impact of A Contribution to Wagtail - Wagtail Space 2025](https://www.youtube.com/watch?v=sW8k4F1DY18&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=19) by Chiemezuo Akujobi. - `2025-11-19`.
- [Wagtail Nest: Maintaining Community Packages Together - Wagtail Space 2025](https://www.youtube.com/watch?v=h0kKy4R5kNY&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=8) by Coen van der Kamp. - `2025-11-19`.
- [Wagtail and AI Agentic Coding - Wagtail Space 2025](https://www.youtube.com/watch?v=pukU8F3ciEM&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=18) by Maciej Baron. - `2025-11-19`.
- [Wagtail in industry: from farming to finance - Wagtail Space 2025](https://www.youtube.com/watch?v=DH87OzXzj28&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=3) by Vince Salvino. - `2025-11-19`.
- [Where next for Wagtail Search? - Wagtail Space 2025](https://www.youtube.com/watch?v=LglWFsqIu3E&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=26) by Matt Westcott. - `2025-11-19`.
- [Who's that code snippet? A screen reader guessing game - Wagtail Space 2025](https://www.youtube.com/watch?v=VkPOe_JixTI&list=PLfwZ-fob20cPI9_fnG_ULYIdOS5TKP1IZ&index=24) by Laura Wissiak and Pawel Masarczyk. - `2025-11-19`.
- [Lightning Talks June 20 - Wagtail Space US 2024](https://www.youtube.com/watch?v=UuE3Y15To8Q&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQ) - lightning talks. - `2024-07-19`.
- [Lightning Talks June 21 - Wagtail Space US 2024](https://www.youtube.com/watch?v=vazMp9jTlEU&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQ) - lightning talks. - `2024-07-19`.
- [Packages! Packages! Packages! - Wagtail Space US 2024](https://www.youtube.com/watch?v=r5ovJPWvxL4&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQ) - panel. - `2024-07-19`.
- [3D Files with Wagtail - Wagtail Space US 2024](https://www.youtube.com/watch?v=ccBrb50xRCM&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQ) by Dawn Wages and Mira Gibson. - `2024-07-19`.
- [Accessibility for Complex Components and Interfaces - Wagtail Space US 2024](https://www.youtube.com/watch?v=AC1gy9R2Z6c&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQ) by Kara Gaulrapp. - `2024-07-19`.
- [Auditing Wagtail Content - Wagtail Space US 2024](https://www.youtube.com/watch?v=a1O3hKib8Ns&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQB&index=2&pp=i) by Will Barton & Chuck Sebian-Lander. - `2024-07-19`.
- [Improving the Editor Experience through Validation - Wagtail Space US 2024](https://www.youtube.com/watch?v=UVBHciwpgKM&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQ) by Scott Cranfill. - `2024-07-19`.
- [PudlStack - Building Wagtail Affinity Group Communities That Offer Bot Helpers - Wagtail Space US 2024](https://www.youtube.com/watch?v=SNEeo_ABQ7g&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQB) by Anthony Garcia. - `2024-07-19`.
- [What Editors Really Want - Wagtail Space US 2024](https://www.youtube.com/watch?v=1qF5wC4rCY4&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQ) by Meagen Voss. - `2024-07-19`.
- [sditail: Extending Wagtail CMS as a Spatial Data Infrastructure - Wagtail Space US 2024](https://www.youtube.com/watch?v=XxdJpYNT4EM&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQ) by César Benjamin. - `2024-07-19`.
- [LLMs and Wagtail - Wagtail Space US 2024](https://www.youtube.com/watch?v=b-luIDn80bc&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQB) by Emily Topp-Mugglestone. - `2024-07-18`.
- [One Thousand and One Wagtail Sites - Wagtail Space US 2024](https://www.youtube.com/watch?v=yciVqzSGWTw&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQB) by Vince Salvino. - `2024-07-18`.
- [Pleasant Publishing Patterns - Wagtail Space US 2024](https://www.youtube.com/watch?v=ZXGcqY-OeYk&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQB) by Michael Trythall. - `2024-07-18`.
- [State of Wagtail - Wagtail Space US 2024](https://www.youtube.com/watch?v=TKLYeKpFbno&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQB) by Tom Dyson. - `2024-07-18`.
- [Wagtail, Reactivated - Headless Without the Headache - Wagtail Space US 2024](https://www.youtube.com/watch?v=mQsI8Ji3_LY&list=PLfwZ-fob20cMduvPwjstgycu-Z_1QwJQB) by Josh Marantz. - `2024-07-18`.
- [Bringing modern authentication to Wagtail: WebAuthn and Passkeys - Wagtail Space NL 2024](https://www.youtube.com/watch?v=qJwg2kFtFW4&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=7) by Storm Heg. - `2024-06-27`.
- [Faster Thumbnails for a Faster Web - Wagtail Space NL 2024](https://www.youtube.com/watch?v=0kHhGBxwzeM&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=5) by Alex Tomkins. - `2024-06-27`.
- [Headless Wagtail Strategies - Wagtail Space NL 2024](https://www.youtube.com/watch?v=nweVHX5DgWU&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=2) by Rémy Sanchez. - `2024-06-27`.
- [How to abuse Wagtail's StreamFields as much as you want - Wagtail Space NL 2024](https://www.youtube.com/watch?v=tOBGJ0riDRw&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=8) by Rémy Sanchez. - `2024-06-27`.
- [Multi-lingual websites in Wagtail - Wagtail Space NL 2024](https://www.youtube.com/watch?v=5rPvOsVeRhA&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=15) by Paul Stevens. - `2024-06-27`.
- [Recovering deleted Django models - Wagtail Space NL 2024](https://www.youtube.com/watch?v=TB64DtQZeB0&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=13) by Jake Howard. - `2024-06-27`.
- [The State of Wagtail - Wagtail Space NL 2024](https://www.youtube.com/watch?v=P9Ftbu5NVUI&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=1) by Tom Dyson. - `2024-06-27`.
- [The impossible art of making everyone happy - Wagtail Space NL 2024](https://www.youtube.com/watch?v=v3KEaMTfKg0&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=6) by Matthew Westcott. - `2024-06-27`.
- [Universal Listings - Wagtail Space NL 2024](https://www.youtube.com/watch?v=aNto27_lfJ4&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=12) by Sage Abdullah. - `2024-06-27`.
- [Wagging HubSpot's Tail - Wagtail Space NL 2024](https://www.youtube.com/watch?v=VUoOoRxlWrU&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=3) by Simon Blanchard and Joost Meijerink. - `2024-06-27`.
- [Wagtail AI and Wagtail Vector Index - Wagtail Space NL 2024](https://www.youtube.com/watch?v=jHuhX_SNF1s&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=9) by Dan Braghiș. - `2024-06-27`.
- [Wagtail Dashboards - Wagtail Space NL 2024](https://www.youtube.com/watch?v=0msxKe0RoNw&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=14) by Judith van Leersum and Emmelien Schiet. - `2024-06-27`.
- [Wagtail Translate - Wagtail Space NL 2024](https://www.youtube.com/watch?v=QxnC70Bwj0k&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=10) by Coen van der Kamp. - `2024-06-27`.
- [Wagtail and Caching - Wagtail Space NL 2024](https://www.youtube.com/watch?v=vBdG2GfAZAo&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=4) by Jake Howard. - `2024-06-27`.
- [You've been caching your content website wrong - Wagtail Space NL 2024](https://www.youtube.com/watch?v=bWF06aCjbUM&list=PLEyaio0l1qoGj7XTEuNXT2o3tYpuSmlbP&index=11) by Rémy Sanchez. - `2024-06-27`.
- [Choosers - Wagtail Space NL 2022](https://www.youtube.com/watch?v=nSjVAISLr4M) by Matthew Westcott. - `2022-06-30`.
- [Digital Nomad - Wagtail Space NL 2022](https://www.youtube.com/watch?v=9Evrwzpg-dw) by Maikel Martens. - `2022-06-30`.
- [Dockerising wagtail projects in 5 minutes - Wagtail Space NL 2022](https://www.youtube.com/watch?v=PgkpBMoN4UY) by Sævar Öfjörð Magnússon. - `2022-06-30`.
- [Moving Wagtail pages - Wagtail Space NL 2022](https://www.youtube.com/watch?v=OFqPKffSVWI) by Viggo de Vries. - `2022-06-30`.
- [The state of Wagtail 2022 - Wagtail Space NL 2022](https://www.youtube.com/watch?v=4D49RENHfoM) by Tom Dyson. - `2022-06-30`.
- [Things I learned - Wagtail Space NL 2022](https://www.youtube.com/watch?v=xG5-s48TZt8) by Dan Braghis. - `2022-06-30`.
- [Unobtrusive internationalisation - Wagtail Space NL 2022](https://www.youtube.com/watch?v=_dhScxTdtjA) by Lars van de Kerkhof. - `2022-06-30`.
- [Wagtail Roadrunner Beep Beep - Wagtail Space NL 2022](https://www.youtube.com/watch?v=ynlFUcutSWQ) by Lars van de Kerkhof. - `2022-06-30`.
- [Wagtail architecture options, or should I go headless - Wagtail Space NL 2022](https://www.youtube.com/watch?v=JMULuz6RzjQ) by Dan Braghis. - `2022-06-30`.
- [Wagtail headless and NextJS frontend - Wagtail Space NL 2022](https://www.youtube.com/watch?v=s8cJhFtjqZA) by Lucas Moeskops. - `2022-06-30`.
- [Wagtail in the News Room - Wagtail Space NL 2022](https://www.youtube.com/watch?v=B85HwmX5uaw) by Sævar Öfjörð Magnússon & Arnar Tumi Þorsteinsson. - `2022-06-30`.
- [Working with Image Filters - Wagtail Space NL 2022](https://www.youtube.com/watch?v=gCGT51BcTdM) by Arnar Tumi Þorsteinsson. - `2022-06-30`.
- [Wagtail Guide - Getting started - Wagtail Space US 2022](https://www.youtube.com/watch?v=E3-kFY6jPPY) by Coen van der Kamp. - `2022-03-31`.
- [5 Things I Learned About Wagtail the Hard Way - Wagtail Space US 2022](https://www.youtube.com/watch?v=LNqVzLkZkig) by Meagen Voss. - `2022-03-30`.
- [A New Approach to Multitenant Wagtail - Wagtail Space US 2022](https://www.youtube.com/watch?v=WN0L4YNrWes) by Stephanie C. Smith and Addison Hardy. - `2022-03-30`.
- [Adding a GraphQL API to Wagtail - Wagtail Space US 2022](https://www.youtube.com/watch?v=_O5isU354vg) by Patrick Arminio. - `2022-03-30`.
- [Bringing JSONField into Wagtail Core - Wagtail Space US 2022](https://www.youtube.com/watch?v=XtazMDNdlK8) by Sage Abdullah. - `2022-03-30`.
- [Designing the new page editor - Wagtail Space US 2022](https://www.youtube.com/watch?v=t2xiPJ91UCE) by Phil Dexter and Ben Enright. - `2022-03-30`.
- [The Wagtail Ecosystem - Wagtail Space US 2022](https://www.youtube.com/watch?v=4Qd43nsxmoc) by Vince Salvino. - `2022-03-30`.
- [The Wagtail Marketplace for Games-based Courses - Wagtail Space 2022](https://www.youtube.com/watch?v=ueou6CxiR3Y) by Sarah Toms. - `2022-03-30`.
- [Tips for Maintaining Wagtail Packages - Wagtail Space US 2022](https://www.youtube.com/watch?v=Zh608nVBrEw) by Tim Allen. - `2022-03-30`.
- [Wagtail Guide - Wagtail Space US 2022](https://www.youtube.com/watch?v=W0tL-5V5BWA) by Coen van der Kamp. - `2022-03-30`.
- [Wagtail as a headless CMS for JavaScript frontends - Wagtail Space US 2022](https://www.youtube.com/watch?v=bYRQ492BED0) by Tommaso Amici. - `2022-03-30`.
- [Wagtail charts and graphs - Wagtail Space US 2022](https://www.youtube.com/watch?v=QK-Vhlpos3Q) by Sævar Öfjörð Magnússon & Arnar Tumi Þorsteinsson. - `2022-03-30`.
- [Wagtail vs. WordPress - Wagtail Space US 2022](https://www.youtube.com/watch?v=Vl2g7H3aodw) by Kalob Taulien. - `2022-03-30`.

### Podcasts

<!-- Add new items at the top. Manually curated over time, never auto-archived. -->

- [Django Chat E9: Wagtail CMS - Tom Dyson](https://djangochat.com/episodes/wagtail-cms-tom-dyson) - An interview with Tom Dyson on Wagtail, the leading Django-based CMS used by tens of thousands of organizations including Google, NASA, and the British NHS. - `2019-04-24`.
- [Django Chat E84: Dawn Wages](https://djangochat.com/episodes/wagtail-react-gatsby-dawn-wages-RaD8k37m) - An interview with Dawn Wages, a core Wagtail team member. Discussion about Wagtail, React and Gatsby. - `2021-02-03`.
- [Django Chat E168: Thibaud Colas](https://djangochat.com/episodes/thibaud-colas-2025-dsf-board-nominations) - An interview with a core team member of Wagtail, discussing the current status of Django, upcoming DSF Board elections, Wagtail roadmap & community opportunities. - `2024-10-16`.

### Videos

<!-- Add new items at the top. Auto-archived after 5 years without updates. -->

- None yet.

### Showcases

<!-- Add new items at the top. Manually curated over time, never auto-archived. -->

- [Made with Wagtail](https://madewithwagtail.org/) - A showcase of sites and apps made with Wagtail CMS. - `2015-04`.
- [Official showcase - Projects made with Wagtail](https://wagtail.org/showcase/) - Curated list of websites and apps that gives you a taste of the very best projects built with Wagtail. - `2024-04`.

### Package lists

<!-- Add new items at the top. Manually curated over time, never auto-archived. -->

- [Wagtail third-party packages](https://wagtail.org/packages/) - Official list based on PyPI data. - `2020-10`.
- [Framework: Wagtail on PyPI](https://pypi.org/search/?c=Framework+%3A%3A+Wagtail) - Packages tagged as `Framework: Wagtail`. - `2026-06`.
- [GitHub: Wagtail topic](https://github.com/topics/wagtail) - Repositories on GitHub tagged with the `wagtail` topic. - `2026-11`.
- [Wagtail grid - Django Packages](https://djangopackages.org/grids/g/wagtail-cms/) - Wagtail projects and packages on Django Packages. - `2017-10`.

## Documentation for editors

- [Mozilla Foundation: How Do I Wagtail?](https://www.mozillafoundation.org/en/docs/how-do-i-wagtail/) - Mozilla's editor facing guide for how to use Wagtail's admin interface.
- [CCA Wagtail Editor Portal](https://portal.cca.edu/help/wagtail-documentation/) - User facing documentation for Wagtail by California College of the Arts
- [Caltech Wagtail Editor Portal](https://sites.caltech.edu/) - User facing documentation for Wagtail by Caltech

## Community

- [Wagtail Space](https://www.wagtail.space/) - Wagtail training sessions, Wagtail (lightning) talks and a Wagtail sprint. From March 13th until 15th 2019, Wagtail Space takes place in Arnhem, The Netherlands.

## Open-source sites

- [Torchbox.com on Wagtail](https://github.com/torchbox/torchbox.com) – Torchbox digital agency website.
- [Federal Election Commission](https://github.com/fecgov/fec-cms) – The content management system (CMS) for the new Federal Election Commission website.
- [Bow Valley SPCA Website](https://github.com/nfletton/bvspca) - Wagtail/Django based website of the Bow Valley SPCA.
- [SecureDrop](https://github.com/freedomofpress/securedrop.org) - Code for the SecureDrop project website.
- [consumerfinance.gov](https://github.com/cfpb/consumerfinance.gov) - Django project protecting American consumers.
- [Western Friend website](https://github.com/WesternFriend/westernfriend.org) - A website for Western Friend (westernfriend.org), a Quaker publication that provides resources and support for Quaker communities and individuals seeking to live out their faith in the world. Western Friend is part of the Religious Society of Friends.
- [Outreachy website](https://github.com/outreachy/website) - Code for the Outreachy website, based on Python, Django, and Bootstrap.
- [Wagtail user guide](https://github.com/wagtail/guide) - A website to teach Wagtail CMS to content editors, moderators and administrators.
- [Penticon Public Library](https://github.com/danlerche/public-library-wagtailCMS) - This is an example public library website using wagtail CMS.

## Contribute

Contributions are always welcome! Please read the [contribution guidelines](https://github.com/wagtail/awesome-wagtail/blob/main/docs/CONTRIBUTING.md) first.

## License

This work by [Springload](https://www.springload.co.nz/) and other contributors is marked [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
