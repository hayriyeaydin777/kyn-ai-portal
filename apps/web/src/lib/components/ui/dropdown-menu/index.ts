import { DropdownMenu as DropdownMenuPrimitive } from 'bits-ui';

const Root = DropdownMenuPrimitive.Root;
const Trigger = DropdownMenuPrimitive.Trigger;
const Group = DropdownMenuPrimitive.Group;

export { default as Content } from './dropdown-menu-content.svelte';
export { default as Item } from './dropdown-menu-item.svelte';
export { default as Label } from './dropdown-menu-label.svelte';
export { default as Separator } from './dropdown-menu-separator.svelte';
export {
	Root,
	Trigger,
	Group,
	Root as DropdownMenu,
	Trigger as DropdownMenuTrigger,
	Group as DropdownMenuGroup
};
