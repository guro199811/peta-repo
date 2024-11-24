const newPet = () => {
  return( 
    <div className="new_pet_box">
        <form>
            <label htmlFor="pet_name">Pet Name</label>
            <input type="text" id="pet_name" required/>
            <label htmlFor="gender">Gender</label>
            <select id="gender" required>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
            </select>
            <label htmlFor="pet_age">Birth Date</label>
            <input type="date" id="pet_age" required/>
            
        </form>
    </div>
  );
};


export default newPet; 