import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <Heading as="h1" className="hero__title">
              {siteConfig.title}
            </Heading>
            <p className="hero__subtitle">{siteConfig.tagline}</p>
            <div className={styles.buttons}>
              <Link
                className="button button--secondary button--lg"
                to="/docs/intro">
                Get Started with the Textbook - 5min ⏱️
              </Link>
            </div>
          </div>
          <div className={styles.heroImage}>
            <img
              src="/img/logo-header.svg"
              alt="Physical AI & Humanoid Robotics"
              className={styles.heroImg}
            />
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="AI Systems in the Physical World - Physical AI & Humanoid Robotics Textbook">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <section className={styles.highlights}>
          <div className="container padding-horiz--md">
            <div className="row">
              <div className="col col--4">
                <div className={styles.highlightCard}>
                  <h3>🤖 Advanced Robotics</h3>
                  <p>Learn cutting-edge techniques in humanoid robotics, sensor integration, and real-world AI applications.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className={styles.highlightCard}>
                  <h3>🌐 Simulation to Reality</h3>
                  <p>Bridge the gap between high-fidelity simulation and real hardware deployment with proven methodologies.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className={styles.highlightCard}>
                  <h3>⚡ Hands-On Learning</h3>
                  <p>Interactive exercises, practical examples, and real-world projects to reinforce your understanding.</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}