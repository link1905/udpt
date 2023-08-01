import { Box, List } from "@mantine/core";
import { NavLink } from "react-router-dom";

export function HomePage() {
  return (
    <Box>
      <List>
        <List.Item>
          <NavLink to="/question">Question list</NavLink>
        </List.Item>
        <List.Item>
          <NavLink to="/question/id">Question detail</NavLink>
        </List.Item>
        <List.Item>
          <NavLink to="/question/create">Create question</NavLink>
        </List.Item>
      </List>
    </Box>
  );
}
