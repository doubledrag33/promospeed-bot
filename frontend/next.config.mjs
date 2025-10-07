import { withPWA } from 'next-pwa';

const nextConfig = withPWA({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
})({
  experimental: {
    serverActions: true,
  },
  images: {
    remotePatterns: [{ protocol: 'https', hostname: '**' }],
  },
});

export default nextConfig;
