import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';

export default function HomePage(): JSX.Element {
  return (
    <Layout
      title="Welcome"
      description="Welcome to {{SITE_NAME}} documentation"
    >
      <main>
        <div className="hero">
          <Heading as="h1" className="hero__title">
            Welcome to {{SITE_NAME}}
          </Heading>
          <p className="hero__subtitle">
            {{SITE_TAGLINE}}
          </p>
          <div className="hero__buttons">
            <Link className="button button--primary" to="/docs/getting-started/installation">
              Get Started
            </Link>
            <Link className="button button--outline" to="/docs/skills-library/overview">
              Explore Skills
            </Link>
          </div>
        </div>

        <div className="features">
          <div className="feature-card">
            <Heading as="h3" className="feature-card__title">
              🚀 Quick Start
            </Heading>
            <p className="feature-card__body">
              Get up and running in minutes with our step-by-step installation guide.
            </p>
          </div>

          <div className="feature-card">
            <Heading as="h3" className="feature-card__title">
              📚 Comprehensive Docs
            </Heading>
            <p className="feature-card__body">
              Detailed guides covering architecture, APIs, deployment, and more.
            </p>
          </div>

          <div className="feature-card">
            <Heading as="h3" className="feature-card__title">
              🔍 Powerful Search
            </Heading>
            <p className="feature-card__body">
              Find what you need quickly with our full-text search functionality.
            </p>
          </div>

          <div className="feature-card">
            <Heading as="h3" className="feature-card__title">
              🎨 Mermaid Diagrams
            </Heading>
            <p className="feature-card__body">
              Visualize complex architectures and flows with built-in diagram support.
            </p>
          </div>

          <div className="feature-card">
            <Heading as="h3" className="feature-card__title">
              💻 Code Examples
            </Heading>
            <p className="feature-card__body">
              Learn by example with syntax-highlighted code snippets in multiple languages.
            </p>
          </div>

          <div className="feature-card">
            <Heading as="h3" className="feature-card__title">
              🔄 Auto-Generated
            </Heading>
            <p className="feature-card__body">
              Documentation stays in sync with your specifications through auto-generation.
            </p>
          </div>
        </div>
      </main>
    </Layout>
  );
}
