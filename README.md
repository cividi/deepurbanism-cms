# Headless Wagtail with Gridsome

This is a boilerplate that demonstrates how to use [Wagtail CMS](https://github.com/wagtail)
with a [Vue.js](https://vuejs.org/) frontend based on [Gridsome](https://gridsome.org/) -
an open source PWA engine with support for GraphQL and other data sources.
The goal of this project is to make it easier to deploy Wagtail as self-hosted headless CMS,
and provide an example frontend compatible with modern CDN platforms.

👋 Say hello in the **#headless** channel on the [Wagtail Slack](https://github.com/wagtail/wagtail/wiki/Slack) 💬

## Inspiration

Investigation into using Wagtail as a "[headless](https://en.wikipedia.org/wiki/Headless_content_management_system)" [CMS](https://jamstack.org/headless-cms/), a mode closely related to [single-page application](https://en.wikipedia.org/wiki/Single-page_application) (SPA), has been discussed for a while. Many people enjoy working with Wagtail, which supports Django's flexible and reliable data models, multiple websites and web service standards out of the box.

Since around version 2.9 there has been increasing interest, with community attempts such as [datalets/blemmy](https://github.com/datalets/blemmy), but still not much official [documentation](https://docs.wagtail.io/en/stable/search.html?q=headless) on how to set up in headless mode. You can use the mature REST APIs as outlined in a 2017 blog post by [Brent Clark](https://wagtail.io/blog/getting-started-with-wagtail-and-graphql/) - or the more edgy GraphQL APIs via [Wagtail Grapple](https://wagtail-grapple.readthedocs.io/en/latest/) as in this project (with [Ariadne](https://ariadnegraphql.org/docs/django-integration) and [Strawberry](https://github.com/strawberry-graphql/strawberry) as top alternatives), discussed among others by [Oliver Sartun](https://wagtail.io/blog/graphql-with-streamfield/).

There are no technical impediments today in the way of an excellent site powered by an edge service with content served headlessly from Wagtail! Recently maintained builds with similar goals include:

- https://github.com/octue/planex-cms (Gatsby, Grapple)
- https://github.com/tbrlpld/wagtail-gatsby-blog-backend (Gatsby, Grapple)
- https://github.com/torchbox/wagtail-headless-preview (React, REST)
- https://gitlab.com/thelabnyc/wagtail-spa-integration (Angular/Next.js)

See also the following presentations on the topic:

- [Wagtail Headless CMS Workshop (with Vue.js)](https://www.youtube.com/watch?v=xUWd3o6z2bk)
- [Wagtail Space US 2018: Michael Harrison, 'Wagtail as a Headless CMS'](https://www.youtube.com/watch?v=HZT14u6WwdY)
- [Gatsby + Wagtail + Netlify (with a little GitPod) – Dawn Wages @ Wagtail Space US 2020](https://www.youtube.com/watch?v=FP907CJsSBk)

_"Wagtail is not an instant website in a box."_ --[Zen of Wagtail](https://github.com/wagtail/wagtail/blob/main/docs/getting_started/the_zen_of_wagtail.md)

# Installation

After you follow the [Deployment](#Deployment) steps below, the Wagtail-Django server will run on port `8000`, while the
Node.js server compiling the Vue.js app will run on port `8080`.

To access the Wagtail admin go to http://localhost:8000/admin/ - and then
login with the superuser you created with the `createsuperuser` command. If the setup
succeeded, you should be able to edit the content of a default home page.

When you switch to the Gridsome frontend in http://localhost:8080 - you should
see the contents you have edited.

The frontend app is expecting a GraphQL API to be available at `localhost:8000/graphql`.
The regular Django API is available at `localhost:8000/api/v2/`.

## Configuration

Create a file at `django/website/wagtail_vue/wagtail_vue/settings/local_dev.py` if you wish to override any settings from `dev.py`.

## Deployment

Deployment with [Docker Compose](https://docs.docker.com/compose/install/) should be rather quick:

`make up`

If anything fails, you can go through the build steps defined in the [Makefile](Makefile):

```
# build image, start and enter container
make refresh

# initialize database (inside container)
django-admin.py migrate
django-admin.py createsuperuser

# start django server (inside container)
django-admin.py runserver 0.0.0.0:8000

# ..or use the handy aliases:
djm
djr

# enter frontend (Gridsome) container
make frontend

# start node server (inside container)
gridsome develop

# stop and remove containers
make clean
```

## Development

The frontend interfaces with Wagtail using the GraphQL API as mentioned above through the [Wagtail Grapple](https://wagtail-grapple.readthedocs.io/en/latest/) library.

![](gridsome/screenshot_graphql.png)

We suggest using Gridsome's default Query tool available at http://localhost:8080/___explore (pictured above). Once you've set up your models and queries, add them to the frontend using Gridsome's [GraphQL data layer](https://gridsome.org/docs/data-layer/) - see [Index.vue](gridsome/src/pages/Index.vue).

Alternatively, use the [Altair GraphQL client](https://altair.sirmuel.design/#download) or similar to connect with the service. A query directly to the GraphQL interface to get page model data might look like this:

```graphql
{
  pages {
    ...on FlexPage {
      title,
      headline,
      body,
      attach {
        rawValue
        ...on ImageChooserBlock {
          image {
            url
          }
        }
      }
    }
  }
}
```

You can generate a [schema.json](schema.json) reflecting the current page model with the following command:

`django-admin graphql_schema`

## Acknowledgements

Thanks to Bryan Hyshka and Kalob Taulien for the project [hyshka/wagtail-vue-talk](https://github.com/hyshka/wagtail-vue-talk) (in [video form here](https://www.youtube.com/watch?v=xUWd3o6z2bk) by Coding For Everybody) which laid many foundations, and to the entire Wagtail team and community for a fantastic product.

[MIT License](LICENSE)
