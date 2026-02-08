import { defineCollection } from 'astro:content';
import { docsSchema } from '@astrojs/starlight/schema';

// Starlight docs collection - uses Starlight's built-in schema
export const collections = {
  docs: defineCollection({ schema: docsSchema() }),
};
