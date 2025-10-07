import { create } from 'zustand';

export interface CartItem {
  id: string;
  productId: string;
  name: string;
  quantity: number;
  bestPrice?: {
    storeName: string;
    price: number;
    sourceType: string;
    capturedAt: string;
  };
}

interface GroptState {
  cart: CartItem[];
  favorites: string[];
  setCart: (items: CartItem[]) => void;
  addFavorite: (id: string) => void;
  removeFavorite: (id: string) => void;
}

export const useGroptStore = create<GroptState>((set) => ({
  cart: [],
  favorites: [],
  setCart: (items) => set({ cart: items }),
  addFavorite: (id) =>
    set((state) => ({ favorites: state.favorites.includes(id) ? state.favorites : [...state.favorites, id] })),
  removeFavorite: (id) => set((state) => ({ favorites: state.favorites.filter((fav) => fav !== id) })),
}));
