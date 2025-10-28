function UserList({ users, loading, onDelete }) {
  if (loading && users.length === 0) {
    return <p>Loading users...</p>;
  }

  if (!loading && users.length === 0) {
    return <p>No users found. Add one above!</p>;
  }

  return (
    <table className="users-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {users.map((user) => (
          <tr key={user.id}>
            <td>{user.id}</td>
            <td>{user.name}</td>
            <td>{user.email}</td>
            <td>
              <button type="button" onClick={() => onDelete(user.id)}>
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default UserList;
